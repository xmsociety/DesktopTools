# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'searchbar.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLineEdit, QPushButton,
    QSizePolicy, QWidget)

class Ui_SearchBar(object):
    def setupUi(self, SearchBar):
        if not SearchBar.objectName():
            SearchBar.setObjectName(u"SearchBar")
        SearchBar.resize(286, 166)
        self.horizontalLayout_2 = QHBoxLayout(SearchBar)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lineEdit = QLineEdit(SearchBar)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setMinimumSize(QSize(0, 32))
        font = QFont()
        font.setFamilies([u"Cascadia Code"])
        self.lineEdit.setFont(font)

        self.horizontalLayout.addWidget(self.lineEdit)

        self.pushButton = QPushButton(SearchBar)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout.addWidget(self.pushButton)


        self.horizontalLayout_2.addLayout(self.horizontalLayout)


        self.retranslateUi(SearchBar)

        QMetaObject.connectSlotsByName(SearchBar)
    # setupUi

    def retranslateUi(self, SearchBar):
        SearchBar.setWindowTitle(QCoreApplication.translate("SearchBar", u"\u5c0f\u547d\u4ee4\u5de5\u5177", None))
        self.lineEdit.setPlaceholderText(QCoreApplication.translate("SearchBar", u"\u6b64\u5904\u952e\u5165\u6587\u5b57\u547d\u4ee4", None))
        self.pushButton.setText(QCoreApplication.translate("SearchBar", u"\u786e\u5b9a", None))
    # retranslateUi

