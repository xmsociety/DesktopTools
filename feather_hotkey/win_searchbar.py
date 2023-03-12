import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QCompleter, QWidget

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
        self.clip_funcs = ClipFuncs(clipboard=self.app.clipboard())
        completer = FuzzyCompleter([i for i in self.clip_funcs.dict_registered.keys()])
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.ui.lineEdit.setCompleter(completer)

    def clip_worker(self):
        cmd = self.ui.lineEdit.text()
        target_symbol = cmd.split(ClipFuncs.SplitSign)[-1]
        self.clip_funcs.replace_spaces(target_symbol)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.hide()
        else:
            super().keyPressEvent(event)

    def closeEvent(self, _):
        print("close~~~~")
        self.close()
