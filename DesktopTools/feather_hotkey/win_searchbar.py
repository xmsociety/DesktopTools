import os

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QAbstractItemView, QCompleter, QWidget

from ..logger import logger
from .clip_string import ClipFuncs, safe_eval
from .ui_searchbar import Ui_SearchBar


class FuzzyCompleter(QCompleter):
    """
    模糊匹配器
    使用方式:
        # region lineEdit completer实现方式
        # completer = FuzzyCompleter(
        #     [i for i in self.clip_funcs.dict_registered.keys()]
        # )
        # completer.setCaseSensitivity(Qt.CaseInsensitive)  # 下拉模式
        # completer.setCaseSensitivity(False)
        # completer.setCompletionMode(QCompleter.InlineCompletion)
        # self.ui.listWidget.setWindowFlags(Qt.Popup)

        # self.ui.lineEdit.setCompleter(completer)
        # endregion
    """

    def __init__(self, words, parent=None):
        super().__init__(words, parent)

    def pathFromIndex(self, index):
        # Return the full path of the selected item
        return self.model().data(index)

    def splitPath(self, path):
        # Return a list of strings that are potential matches for the input
        return [
            word for word in self.model().stringList() if (
                path.lower() in word.lower()
            )
        ]

class WinSearchBar(QWidget):
    """
    功能搜索框
    """
    SignCommand = "eval 执行它(请仔细核对命令,并知晓后果)"
    Record_KV = "记录kv"
    Read_KV = "读取kv"

    def __init__(self, app=None, tray=None, dict_windows={}, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_SearchBar()
        self.ui.setupUi(self)
        self.app = app
        self.tray = tray
        self.dict_windows = dict_windows
        self.dict_colon_func = {
            WinSearchBar.Record_KV: self.record_kv,
            WinSearchBar.Read_KV: self.read_kv,
        }
        self.ui.pushButton.setDefault(True)
        self.ui.listWidget.hide()
        self.clip_funcs = ClipFuncs(clipboard=self.app.clipboard())
        self.ui.listWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.pushButton.clicked.connect(self.clip_worker)
        self.ui.lineEdit.textChanged.connect(self.handleTextChange)
        self.ui.listWidget.clicked.connect(self.on_listWidget_clicked)
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

    def on_listWidget_clicked(self, index):
        """
        下拉候选项被点击时的处理动作
        点击 下拉选项
        """
        completion_text = index.data()
        if completion_text in set(self.dict_windows.keys()):
            self.dict_windows[completion_text].show()
            self.hide()
        elif completion_text in set(self.dict_colon_func.keys()):
            self.dict_colon_func[completion_text]()
            self.hide()
        elif ": " in completion_text and (completion_text.split(": ")[0]
                                          in set(self.dict_colon_func.keys())):
            func_key, content = completion_text.split(": ")
            self.dict_colon_func[func_key](content)
            self.hide()
        elif completion_text == self.SignCommand:
            try:
                exec(self.command)
            except Exception as err:
                self.tray.show_warning_msg(f"代码有误: {err}")
        else:
            self.ui.lineEdit.setText(completion_text)

    def like_eval_command(self, text) -> bool:
        try:
            self.command = compile(text, "<string>", "exec")  # 执行 没有返回值
            # self.command = compile(text, "<string>", "eval") # 求值import语句无法执行
            return True
        except Exception:
            return False

    def like_kv(self, mode, text) -> bool:
        """eg: /k: v
        arg:
           mode in ("record", "read")
        """
        try:
            if text and mode == "record" and text[0] == '/' and ": " in text:
                return True
            elif text and mode == "read" and text[0] == '/':
                return True
            return False
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

    def record_kv(self, completion_text=None):
        # TODO 将KV写入数据库
        self.tray.show_info_msg("写入kv成功...")

    def read_kv(self, content=None):
        # TODO 从数据库读取可能的key和value
        self.tray.show_info_msg(f"使用{content}读取kv...")

    def get_eval_command_rst(self, text):
        """获取eval结果"""
        rst = safe_eval(text)
        if isinstance(rst, int) or isinstance(rst, float):
            return f"计算结果是: {rst}"
        else:
            return self.SignCommand

    def show_completions(self, text: str):
        """
        显示搜索框下推listWidget荐项
        向 `list_model` 中写入数据
        """
        list_model = []
        self.ui.listWidget.clear()
        # 预置函数计算结果
        list_clip_rst = self.clip_funcs.list_all_result(text)
        list_model.extend([i.result for i in list_clip_rst])
        # 打开窗口
        if self.like_open_windows(text=text):
            list_model += list(self.dict_windows.keys())
        # 计算结果
        if self.like_eval_command(text=text):
            list_model.append(self.get_eval_command_rst(text))
        # 显示k-y(存储和读取)
        if self.like_kv(mode="record", text=text):
            # 存储
            list_model.append(WinSearchBar.Record_KV)
        elif self.like_kv(mode="read", text=text):
            # TODO 读取 相近的key
            list_model.append(WinSearchBar.Read_KV + ": " + "todo read from db")

        self.ui.listWidget.addItems(list_model)
        if self.ui.listWidget.model().rowCount() == 0:
            self.ui.listWidget.hide()
        else:
            self.ui.listWidget.show()
            self.ui.listWidget.setCurrentIndex(
                self.ui.listWidget.model().index(0, 0)
            )

    def handleTextChange(self):
        text = self.ui.lineEdit.text()
        if text:
            self.show_completions(text)
        else:
            self.ui.listWidget.hide()

    def clip_worker(self):
        cmd = self.ui.lineEdit.text()
        logger.info(f"run cmd is: {cmd}")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.hide()
        else:
            super().keyPressEvent(event)

    def closeEvent(self, _):
        self.close()
