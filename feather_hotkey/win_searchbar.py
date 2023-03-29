import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QCompleter, QWidget

from logger import logger
from .clip_string import ClipFuncs
from .ui_searchbar import Ui_SearchBar


class FuzzyCompleter(QCompleter):
    """
    模糊匹配器
    """

    def __init__(self, words, parent=None):
        super().__init__(words, parent)

    def pathFromIndex(self, index):
        # Return the full path of the selected item
        return self.model().data(index)

    def splitPath(self, path):
        # Return a list of strings that are potential matches for the input
        return [
            word for word in self.model().stringList() if path.lower() in word.lower()
        ]


class WinSearchBar(QWidget):
    """
    功能搜索框
    """

    def __init__(self, app=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_SearchBar()
        self.ui.setupUi(self)
        self.app = app
        # self.ui.pushButton.clicked.connect(lambda: self.click_2())
        self.ui.pushButton.clicked.connect(self.clip_worker)
        self.ui.pushButton.setDefault(True)
        self.clip_funcs = ClipFuncs(clipboard=self.app.clipboard())
        completer = FuzzyCompleter(
            [i for i in self.clip_funcs.dict_registered.keys()]
        )
        # self.setStyle()
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.ui.lineEdit.setCompleter(completer)

    def setStyle(self):
        # self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def unregistered_warning(self, *arg, **kwargs):
        self.ui.lineEdit.setText("命令错误-没有匹配到处理方法")
        return False, "命令错误-没有匹配到处理方法"

    def clip_worker(self):
        cmd = self.ui.lineEdit.text()
        logger.info(f"run cmd is: {cmd}")

        registered_key = cmd
        ok, err = True, ''
        try:
            if ClipFuncs.SplitSign in cmd:
                registered_key, target_symbol = cmd.split(ClipFuncs.SplitSign)
                ok, err = self.clip_funcs.dict_registered.get(
                    registered_key+ClipFuncs.SplitSign, self.unregistered_warning
                )(
                    target_symbol=target_symbol
                )
            else:
                ok, err = self.clip_funcs.dict_registered.get(
                    registered_key, self.unregistered_warning)()
            if not ok:
                self.ui.lineEdit.setText(err)
            else:
                self.hide()
        except Exception as err:
            self.ui.lineEdit.setText(str(err))
            logger.error(f"clip_worker Error: {err}")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.hide()
        else:
            super().keyPressEvent(event)

    def closeEvent(self, _):
        self.close()
