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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLineEdit, QListWidget,
    QListWidgetItem, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_SearchBar(object):
    def setupUi(self, SearchBar):
        if not SearchBar.objectName():
            SearchBar.setObjectName(u"SearchBar")
        SearchBar.setEnabled(True)
        SearchBar.resize(701, 280)
        SearchBar.setStyleSheet(u"            background-color: #F9F9F9;\n"
"            color: #333333;\n"
"            font-size: 16px;\n"
"            font-family: Arial, sans-serif;")
        self.horizontalLayout_2 = QHBoxLayout(SearchBar)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.lineEdit = QLineEdit(SearchBar)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setStyleSheet(u"            background-color: #FFFFFF;\n"
"            border-radius: 40px;\n"
"            border: 2px solid #CCCCCC;\n"
"            padding: 20px;\n"
"            font-size: 18px;\n"
"            font-family: Arial, sans-serif;")

        self.horizontalLayout_3.addWidget(self.lineEdit)

        self.pushButton = QPushButton(SearchBar)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setStyleSheet(u"            background-color: #008CBA;\n"
"            border-radius: 40px;\n"
"            border: none;\n"
"            padding: 20px 40px;\n"
"            font-size: 18px;\n"
"            font-family: Arial, sans-serif;\n"
"            color: #FFFFFF;")

        self.horizontalLayout_3.addWidget(self.pushButton)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.listWidget = QListWidget(SearchBar)
        QListWidgetItem(self.listWidget)
        QListWidgetItem(self.listWidget)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setLayoutDirection(Qt.LeftToRight)
        self.listWidget.setStyleSheet(u"background-color: #FFFFFF;\n"
"border-radius: 16px;\n"
"border: 2px solid #CCCCCC;\n"
"padding: 20px;\n"
"font-size: 20px;\n"
"font-family: Arial, sans-serif;\n"
"line-height: 2.5;\n"
"margin-bottom: 10px;	\n"
"margin: 1px; ")

        self.verticalLayout.addWidget(self.listWidget)


        self.horizontalLayout_2.addLayout(self.verticalLayout)


        self.retranslateUi(SearchBar)

        self.listWidget.setCurrentRow(0)


        QMetaObject.connectSlotsByName(SearchBar)
    # setupUi

    def retranslateUi(self, SearchBar):
        SearchBar.setWindowTitle(QCoreApplication.translate("SearchBar", u"\u5c0f\u547d\u4ee4\u5de5\u5177", None))
        self.lineEdit.setPlaceholderText(QCoreApplication.translate("SearchBar", u"\u5f00\u59cb\u8f93\u5165\u547d\u4ee4...", None))
        self.pushButton.setText(QCoreApplication.translate("SearchBar", u"\u786e\u5b9a", None))

        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        ___qlistwidgetitem = self.listWidget.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("SearchBar", u"\u4f60\u597d", None));
        ___qlistwidgetitem1 = self.listWidget.item(1)
        ___qlistwidgetitem1.setText(QCoreApplication.translate("SearchBar", u"hello", None));
        self.listWidget.setSortingEnabled(__sortingEnabled)

    # retranslateUi

