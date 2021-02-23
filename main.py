#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Pendulum PyQt5 Main

Create a simple window in PyQt5.

author: Ian Vzs
website: https://github.com/IanVzs/Halahayawa
Last edited: 22 2 2021
"""
import sys
# from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget
# from PyQt5.QtGui import QIcon, QFont
from PySide2 import QtCore
from PySide2.QtWidgets import QApplication, QWidget
from PySide2.QtGui import QIcon, QFont, QGuiApplication


class Main(QWidget):

    def __init__(self, screen=False):
        super().__init__()

        self.screen = screen
        self.initUI()


    def initUI(self):

        # self.tooltip()
        # self.setGeometry(300, 300, 300, 220)
        self.center()
        self.setWindowTitle('Pendulum')
        self.setWindowIcon(QIcon('harry_potter.png'))

        self.show()

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
        from PyQt5.QtWidgets import QMessageBox
        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes | 
            QMessageBox.No, QMessageBox.No)

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
