#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Pendulum PySide2 Main

Create a simple window in PySide2.

author: Ian Vzs
website: https://github.com/IanVzs/Halahayawa
Last edited: 22 2 2021
"""
import sys
# from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget
# from PyQt5.QtGui import QIcon, QFont
from PySide2.QtCore import QTimer, QThread
from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QMessageBox, QPushButton
from PySide2.QtGui import QIcon, QFont, QGuiApplication

from tools import time_now, datetime2str
from monitor import ThreadSignal, SignalKeyboard


class Main(QWidget):

    def __init__(self, screen=False):
        super().__init__()

        self.screen = screen
        self.initUI()
        self.initTimer()
        SignalKeyboard()


    def initTimer(self):
	# 定时器
        self.timer = QTimer()
        self.timer.timeout.connect(self.timeWorking)
        self.timer.start(1 * 1000) # 1s

    def timeWorking(self):
        self.dictLabels["vtimeCounter"].setText(time_now())

    def initUI(self):

        # self.tooltip()
        # self.setGeometry(300, 300, 300, 220)
        self.center()
        self.setWindowTitle('Pendulum')
        self.setWindowIcon(QIcon('harry_potter.png'))

        self.vbox, self.hbox, self.hbox2 = self.initBoxLayout()
        self.initMainWidgets()

        self.hbox.addWidget(self.dictLabels["timeCounter"])
        self.hbox.addWidget(self.dictLabels["vtimeCounter"])
        self.hbox2.addWidget(self.dictButtons["123"])
        self.hbox2.addWidget(self.dictButtons["abc"])

        self.vbox.addLayout(self.hbox)
        self.vbox.addLayout(self.hbox2)
        self.setLayout(self.vbox)

        self.show()

    def initBoxLayout(self):
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        hbox2 = QHBoxLayout()
        return vbox, hbox, hbox2

    def initMainWidgets(self):
        self.dictLabels = {
            "timeCounter": QLabel("现在时间: "),
            "vtimeCounter": QLabel(""),
        }
        a1 = QPushButton(">123", self)
        a2 = QPushButton(">abc", self)
        a1.clicked.connect(lambda: self.click_1(a1))
        a2.clicked.connect(lambda: self.click_2(a2))
        self.dictButtons = {
            "123": a1,
            "abc": a2,
        }

    def click_1(self, button):
        button.setEnabled(False)
        self.thread_1 = ThreadSignal()  # 创建线程
        self.thread_1._signal.connect(lambda: self.enableButton(button))
        self.thread_1.start()  # 开始线程

    def click_2(self, button):
        button.setEnabled(False)
        self.thread_2 = ThreadSignal()
        self.thread_2._signal.connect(lambda: self.enableButton(button))
        self.thread_2.start()
    
    def enableButton(self, button):
        button.setEnabled(True)

    def tooltip(self):
        """提示框  不过不好使唤"""
        from PyQt5.QtWidgets import QPushButton, QToolTip
        QToolTip.setFont(QFont('SansSerif', 10))

        self.setToolTip('This is a <b>QWidget</b> widget')

        btn = QPushButton('Button', self)
        btn.setToolTip('This is a <b>QPushButton</b> widget')
        btn.resize(btn.sizeHint())
        # btn.move(50, 50)

    def closeEvent(self, event):
        """退出确认"""
        # TODO 测试期嫌累
        return 
        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes | 
            QMessageBox.No, QMessageBox.Yes)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def center(self):
        """
            居中
            PyQt5 没消息
            PySide2 提示DeprecationWarning: QDesktopWidget.availableGeometry(int screen) const is deprecated
        """
        # region Qt5
        # from PySide2.QtWidgets import QDesktopWidget
        # qr = self.frameGeometry()
        # cp = QDesktopWidget().availableGeometry().center()
        # qr.moveCenter(cp)
        # self.move(qr.topLeft())
        #endregion

        size = self.geometry()
        screen = self.screen
        self.move((screen.width() - size.width()) / 2,
            (screen.height() - size.height()) / 2)
        # 此方法不警告了,不过多屏居中会..居中在所有屏幕总和的中间


if __name__ == '__main__':

    app = QApplication(sys.argv)
    screen = app.primaryScreen().geometry()
    ex = Main(screen)
    sys.exit(app.exec_())
