#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Pendulum PySide6 Main

Create a simple window in PySide6.

author: Ian Vzs
website: https://github.com/IanVzs/Halahayawa
Last edited: 22 2 2021
"""
import time

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMessageBox, QWidget

from .app.msg_systray import TrayIcon
from .feather_hotkey.thread import SignalHotKey
from .feather_hotkey.win_searchbar import WinSearchBar
from .feather_timer.halahayawa import WinHowLongHadYouWork
from .logger import logger

# from PySide6.QtGui import QFont, QIcon


class WinMain(QWidget):
    """
    虚假的主窗口
    所有的子`QWidget`理论上都可以独立运行
    """

    def __init__(self, screen=False, app=None):
        super().__init__(None)

        self.screen = screen
        self.tray = TrayIcon(self)

        self.win_timer = WinHowLongHadYouWork(screen, self.tray)
        dict_win_feather = {"工作时长": self.win_timer}
        self.win_searchbar = WinSearchBar(app, self.tray, dict_win_feather)

        self.initSearchBar()

        # self.win_timer.show()
        self.tray.show()

    def initSearchBar(self):
        """
        使用线程初始化SearchBar, 在线程中绑定热键
        """
        thread_hotkey = SignalHotKey()
        thread_hotkey._signal.connect(self.open_search_bar)
        time.sleep(0.5)  # 此处继续sleep防止mac下出错 - 未验证
        thread_hotkey.listen()
        logger.debug("will show")

    def open_search_bar(self):
        self.win_searchbar.setWindowFlags(Qt.WindowStaysOnTopHint)
        if not self.win_searchbar.isVisible():
            self.win_searchbar.setStyle()
            self.win_searchbar.show()
        self.win_searchbar.activateWindow()

    def closeEvent(self, event):
        """退出确认"""
        # TODO 测试期嫌累
        self.win_searchbar.close()
        self.win_timer.close()
        return
        reply = QMessageBox.question(
            self,
            "Message",
            "Are you sure to quit?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.Yes,
        )

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
