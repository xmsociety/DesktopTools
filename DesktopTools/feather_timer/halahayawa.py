#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Pendulum PySide6 Main

Create a simple window in PySide6.

author: Ian Vzs
website: https://github.com/IanVzs/Halahayawa
Last edited: 22 2 2021
"""
import os
import sys
import time
import random
import psutil
# from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget
# from PyQt5.QtGui import QIcon, QFont
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QIcon
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ..args import MOUSE  # Alert_LockWorkStation_MSG,
from ..args import (
    KEYBOARD,
    Alert_REST_KEEP_MSG,
    Alert_REST_MSG,
    Alert_REST_MUST_MSG,
    KEYBOARD_DeviceNo,
    MOUSE_DeviceNo,
    NUM_REST_KEEP_Alert,
    args,
)
from ..logger import slogger
from ..tools import lenth_time, lock_work_station, time_now
from . import input_counter
from .data_alchemy.models import WorkInfo
from .monitor import AlertDict, SignalKeyboard, SignalMouse, ThreadSignal, WorkDict
from ..app.msg_systray import TrayIcon


class WinHowLongHadYouWork(QWidget):
    def __init__(self, screen=False, tray: TrayIcon=None):
        super().__init__(None)

        self.screen = screen
        self.work_dict = WorkDict()
        self.tray = tray
        self.initUI()
        self.initTimer()
        self.initMonitor()

    def iamworking(self, by: str = ""):
        self.work_dict.last_time = time.time()
        if KEYBOARD == by:
            self.work_dict.fill_work_by(KEYBOARD_DeviceNo)
        elif MOUSE == by:
            self.work_dict.fill_work_by(MOUSE_DeviceNo)
        else:
            slogger.error(f"working can't by {by}")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.hide()
        else:
            super().keyPressEvent(event)

    def initMonitor(self):
        thread_kbd = SignalKeyboard()
        thread_mouse = SignalMouse()

        thread_kbd._signal.connect(lambda: self.iamworking(KEYBOARD))
        thread_mouse._signal.connect(lambda: self.iamworking(MOUSE))

        thread_kbd.listen()
        # MacOS 怕不是个傻子... 以下sleep修复了`AttributeError: CFMachPortCreateRunLoopSource`
        # 也可能我是个😳😳
        time.sleep(0.5)
        thread_mouse.listen()

    def show_rest_msg(self):
        # 判断条件&显示提醒
        line = self.work_dict.status_continued.get(WorkInfo.type_map_reverse["工作"], 0)
        slogger.debug(f"check rest alert: line: {line}, threshold: {args.threshold}")
        if line >= args.threshold * 60 and line <= args.threshold * 60 * 1.5:
            AlertDict.alert_rest = True
            self.tray.showYouNeedRest(Alert_REST_MSG, 2)
            slogger.warning("alert show: rest >")
        elif line >= args.threshold * 60 * 1.5:
            AlertDict.alert_rest = True
            self.tray.showYouNeedRest(Alert_REST_MUST_MSG, 3)
            slogger.warning("alert show: rest must >")
            lock_work_station()
        elif AlertDict.alert_rest:
            self.tray.showYouNeedRest(Alert_REST_KEEP_MSG, 1)
            AlertDict.keep_num -= 1
            if AlertDict.keep_num <= 0:
                AlertDict.alert_rest = False
                AlertDict.keep_num = NUM_REST_KEEP_Alert
            slogger.info("alert show: rest keep <")
        # TODO 增加锁屏功能 elif line >= 1 * 60:
        # self.tray.showYouNeedRest(Alert_LockWorkStation_MSG, 1)
        # lock_work_station()

    def initTimer(self):
        # 定时器
        self.dictLabels["workAll"].setText("已经持续工作: 0s\n本次总工作: 0s")
        self.dictLabels["restAll"].setText("已经休息: 0s\n本次总小憩: 0s")
        self.timer = QTimer()
        self.timerRest = QTimer()
        self.timer.timeout.connect(self.timeWorking)
        self.timerRest.timeout.connect(self.show_rest_msg)
        self.timer.start(1 * 1000)  # 1s
        self.timerRest.start(60 * 1000)  # 60s

    def timeWorking(self):
        self.work_dict.summarize()

        self.dictLabels["vtimeNow"].setText(time_now())

        work_tm = self.work_dict.status_continued.get(
            WorkInfo.type_map_reverse["工作"], 0
        )
        rest_tm = self.work_dict.status_continued.get(
            WorkInfo.type_map_reverse["小憩"], 0
        )
        if work_tm:
            self.dictLabels["workAll"].setText(
                f"已经持续工作: {lenth_time(work_tm)}\n本次总工作: {lenth_time(self.work_dict.work_all)}"
            )
        elif rest_tm:
            self.dictLabels["restAll"].setText(
                f"已经休息: {lenth_time(rest_tm)}\n本次总小憩: {lenth_time(self.work_dict.rest_time)}"
            )
        if random.random() < 0.3:
            # 0.3的可能性计算电脑资源信息
            # 获取系统内存信息
            memory_info = psutil.virtual_memory()
            memory_info_dict = {
                "总内存": f"{memory_info.total / (1024 ** 3):.2f} GB",
                "已用内存": f"{memory_info.used / (1024 ** 3):.2f} GB",
                "可用内存": f"{memory_info.available / (1024 ** 3):.2f} GB",
                "空闲内存": f"{memory_info.free / (1024 ** 3):.2f} GB",
                "内存使用率": f"{memory_info.percent}%",
            }
            percpu_percent = psutil.cpu_percent(percpu=True, interval=0)  # interval=1 表示计算1秒钟内的CPU使用率
            warning_msg = ""
            if memory_info_dict["内存使用率"] > "90%":
                warning_msg += f"内存使用率过高,注意排查: {memory_info_dict['内存使用率']}"
            if sum(percpu_percent) > len(percpu_percent) * 50:
                warning_msg += f"cpu使用率过高,系统将操作缓慢: {percpu_percent.join(',')}"
            if warning_msg:
                slogger.warning(warning_msg)
                self.tray.show_warning_msg(warning_msg)
    def initUI(self):
        # self.tooltip()
        # self.setGeometry(300, 300, 300, 220)
        self.center()
        self.setWindowTitle("Pendulum")

        # 设置图标
        ico_path = ""
        if os.path.exists("harry_potter.ico"):
            ico_path = "harry_potter.ico"
        else:
            app_path = os.path.dirname(os.path.abspath(__file__))
            root_path, feather_fname = os.path.split(app_path)
            if feather_fname.startswith("feather"):
                ico_path = os.path.join(root_path, "harry_potter.ico")
        self.setWindowIcon(QIcon(ico_path))
        # self.setWindowIcon(QIcon("harry_potter.ico"))

        self.vbox, self.hbox, self.hbox2, self.hbox3 = self.initBoxLayout()
        self.initMainWidgets()

        self.hbox.addWidget(self.dictLabels["timeNow"])
        self.hbox.addWidget(self.dictLabels["vtimeNow"])
        self.hbox2.addWidget(self.dictLabels["workAll"])
        self.hbox2.addWidget(self.dictLabels["restAll"])
        self.hbox3.addWidget(self.dictButtons["123"])
        self.hbox3.addWidget(self.dictButtons["abc"])

        self.vbox.addLayout(self.hbox)
        self.vbox.addLayout(self.hbox2)
        self.vbox.addLayout(self.hbox3)
        self.setLayout(self.vbox)

        # self.show()

    def initBoxLayout(self):
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        hbox2 = QHBoxLayout()
        hbox3 = QHBoxLayout()
        return vbox, hbox, hbox2, hbox3

    def initMainWidgets(self):
        self.dictLabels = {
            "timeNow": QLabel("现在时间: "),
            "vtimeNow": QLabel(""),
            "workAll": QLabel(""),
            "restAll": QLabel(""),
        }
        a1 = QPushButton("couner", self)
        a2 = QPushButton(">abc", self)

        # a1.clicked.connect(lambda: self.click_1(a1))
        a1.clicked.connect(lambda: input_counter.show_count(self.screen))
        a2.clicked.connect(lambda: self.click_2(a2))
        self.dictButtons = {
            "123": a1,
            "abc": a2,
        }

    def click_2(self, button):
        button.setEnabled(False)
        self.thread_2 = ThreadSignal()  # 创建线程
        self.thread_2._signal.connect(lambda: self.enableButton(button))  # 借用lambda实现带参
        self.thread_2.start()  # 开始线程

    def enableButton(self, button):
        button.setEnabled(True)

    def tooltip(self):
        """提示框  不过不好使唤"""
        from PyQt5.QtWidgets import QPushButton, QToolTip

        QToolTip.setFont(QFont("SansSerif", 10))

        self.setToolTip("This is a <b>QWidget</b> widget")

        btn = QPushButton("Button", self)
        btn.setToolTip("This is a <b>QPushButton</b> widget")
        btn.resize(btn.sizeHint())
        # btn.move(50, 50)

    def center(self):
        """
        居中
        PyQt5 没消息
        PySide6 提示DeprecationWarning: QDesktopWidget.availableGeometry(int screen) const is deprecated
        """
        # region Qt5
        # from PySide6.QtWidgets import QDesktopWidget
        # qr = self.frameGeometry()
        # cp = QDesktopWidget().availableGeometry().center()
        # qr.moveCenter(cp)
        # self.move(qr.topLeft())
        # endregion

        size = self.geometry()
        screen = self.screen
        self.move(
            (screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2
        )
        # 此方法不警告了,不过多屏居中会..居中在所有屏幕总和的中间

    def closeEvent(self, event):
        """
        点击x关闭窗口时
        如果不ignore掉该信号的话会导致主进程退出
        """
        self.hide()
        event.ignore()


if __name__ == "__main__":
    """这段应该不能正常运行了, 有空儿再琢磨下怎么单模块测试"""
    app = QApplication(sys.argv)
    screen = app.primaryScreen().geometry()
    ex = WinHowLongHadYouWork(screen, app=app)
    sys.exit(app.exec())
