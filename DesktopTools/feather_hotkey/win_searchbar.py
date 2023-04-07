import os

from PySide6.QtCore import QStringListModel, Qt
from PySide6.QtGui import QIcon, QStandardItem, QStandardItemModel
from PySide6.QtWidgets import QAbstractItemView, QCompleter, QWidget

from ..logger import logger
from .clip_string import ClipFuncs, safe_eval
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
    SignCommand = "eval 执行它(请仔细核对命令,并知晓后果)"

    def __init__(self, app=None, tray=None, dict_windows={}, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_SearchBar()
        self.ui.setupUi(self)
        self.app = app
        self.tray = tray
        self.dict_windows = dict_windows
        # self.ui.pushButton.clicked.connect(lambda: self.click_2())
        self.ui.pushButton.setDefault(True)
        self.ui.listView.hide()
        self.clip_funcs = ClipFuncs(clipboard=self.app.clipboard())
        # region lineEdit completer实现方式
        completer = FuzzyCompleter([i for i in self.clip_funcs.dict_registered.keys()])
        completer.setCaseSensitivity(Qt.CaseInsensitive)  # 下拉模式
        # completer.setCaseSensitivity(False)
        # completer.setCompletionMode(QCompleter.InlineCompletion)
        # self.ui.listView.setWindowFlags(Qt.Popup)
        # endregion
        self.ui.lineEdit.setCompleter(completer)
        self.ui.listView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.pushButton.clicked.connect(self.clip_worker)
        self.ui.lineEdit.textChanged.connect(self.handleTextChange)
        self.ui.listView.clicked.connect(self.on_listView_clicked)
        self.command = None
        self.set_icon()

    def set_icon(self):
        """设置图标"""
        ico_path = ""
        if os.path.exists("harry_potter.ico"):
            ico_path = "harry_potter.ico"
        else:
            app_path = os.path.dirname(os.path.abspath(__file__))
            root_path, feather_fname = os.path.split(app_path)
            if feather_fname.startswith("feather"):
                ico_path = os.path.join(root_path, "harry_potter.ico")
        self.setWindowIcon(QIcon(ico_path))

    def setStyle(self):
        # self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def unregistered_warning(self, *arg, **kwargs):
        self.ui.lineEdit.setText("命令错误-没有匹配到处理方法")
        return False, "命令错误-没有匹配到处理方法"

    def on_listView_clicked(self, index):
        """
        下拉候选项被点击时的处理动作
        """
        completion_text = index.data()
        if completion_text in set(self.dict_windows.keys()):
            self.dict_windows[completion_text].show()
            self.hide()
        elif completion_text == self.SignCommand:
            try:
                exec(self.command)
            except Exception as err:
                self.tray.show_warning_msg(f"代码有误: {err}")
        else:
            self.ui.lineEdit.setText(completion_text)
        # selistView.hide()

    def like_eval_command(self, text) -> bool:
        try:
            self.command = compile(text, "<string>", "exec")  # 执行 没有返回值
            # self.command = compile(text, "<string>", "eval") # 求值import语句无法执行
            return True
        except Exception:
            return False

    def like_open_windows(self, text) -> bool:
        """
        判断输入文本是否是想要打开功能窗口
        """
        # TODO 有待优化
        all_win_key = "".join([i for i in self.dict_windows.keys()])
        if text in all_win_key:
            return True
        return False

    def show_completions(self, text):
        """
        显示搜索框下推listView荐项
        """
        list_model = ["apple", "banana", "cherry", "aaaaa!"]
        list_model = [i for i in list_model if i.lower().startswith(text.lower())]
        if self.like_open_windows(text=text):
            list_model += list(self.dict_windows.keys())
        if self.like_eval_command(text=text):
            rst = safe_eval(text)
            if isinstance(rst, int) or isinstance(rst, float):
                list_model.append(f"计算结果是: {rst}")
            else:
                list_model.append(self.SignCommand)
        self.ui.listView.setModel(QStringListModel(list_model))
        # completer_list = ["apple", "banana", "cherry", "aaaaa!"]
        self.ui.listView.model().setStringList(list_model)
        if self.ui.listView.model().rowCount() == 0:
            self.ui.listView.hide()
        else:
            self.ui.listView.show()
            self.ui.listView.setCurrentIndex(self.ui.listView.model().index(0, 0))

    def handleTextChange(self):
        text = self.ui.lineEdit.text()
        if text:
            # self.ui.listView.show()
            self.show_completions(text)
            # model = QStandardItemModel()
            # model.setHorizontalHeaderLabels([''])
            # item = QStandardItem('这里是静态文本')
            # item.setTextAlignment(Qt.AlignCenter)
            # model.setItem(0, 0, item)
            # self.ui.listView.setModel(model)
        else:
            self.ui.listView.hide()

    def clip_worker(self):
        cmd = self.ui.lineEdit.text()
        logger.info(f"run cmd is: {cmd}")

        registered_key = cmd
        ok, err = True, ""
        try:
            if ClipFuncs.SplitSign in cmd:
                registered_key, target_symbol = cmd.split(ClipFuncs.SplitSign)
                ok, err = self.clip_funcs.dict_registered.get(
                    registered_key + ClipFuncs.SplitSign, self.unregistered_warning
                )(target_symbol=target_symbol)
            else:
                ok, err = self.clip_funcs.dict_registered.get(
                    registered_key, self.unregistered_warning
                )()
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
