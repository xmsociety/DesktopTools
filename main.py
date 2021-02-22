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
from PyQt5.QtWidgets import QApplication, QWidget


if __name__ == '__main__':

    app = QApplication(sys.argv)
    w = QWidget()

    # w.resize(250, 150)
    # w.move(300, 300)
    w.setWindowTitle('Pendulum')
    w.show()

    sys.exit(app.exec_())
