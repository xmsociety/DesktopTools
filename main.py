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
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget
from PyQt5.QtGui import QIcon, QFont


class Main(QWidget):

    def __init__(self):
        super().__init__()

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
        """居中"""
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Main()
    sys.exit(app.exec_())
