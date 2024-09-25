import os
import sys

from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QMenu, QSystemTrayIcon


class TrayIcon(QSystemTrayIcon):
    """
    系统托盘图标定义
    """

    def __init__(self, parent=None):
        super(TrayIcon, self).__init__(parent)
        self.showMenu()
        self.initConnect()

    def showMenu(self):
        """
        设计托盘的菜单
        """
        self.menuMain = QMenu()

        self.action_test = QAction("测试休息提醒消息", self, triggered=self.showYouNeedRest)
        self.subMenu = QMenu()
        self.subMenu.setTitle("测试菜单")
        self.subMenu.addAction(self.action_test)
        self.menuMain.addMenu(
            self.subMenu,
        )

        self.action_quit = QAction("退出", self, triggered=self.quit)
        self.action_search_bar = QAction("搜索", self, triggered=self.show_search_bar)
        self.menuMain.addAction(self.action_search_bar)
        self.menuMain.addAction(self.action_quit)
        
        self.setContextMenu(self.menuMain)

    def initConnect(self):
        # 把鼠标点击图标的信号和槽连接
        self.activated.connect(self.iconClicked)

        # 把鼠标点击弹出消息的信号和槽连接
        self.messageClicked.connect(self.msgClickEvent)

        # 设置图标
        ico_path = ""
        if os.path.exists("harry_potter.ico"):
            ico_path = "harry_potter.ico"
        else:
            app_path = os.path.dirname(os.path.abspath(__file__))
            root_path, app_fname = os.path.split(app_path)
            if app_fname == "app":
                ico_path = os.path.join(root_path, "harry_potter.ico")
        self.setIcon(QIcon(ico_path))
        self.icon = self.MessageIcon(QSystemTrayIcon.MessageIcon.NoIcon)

    def iconClicked(self, reason):
        "鼠标点击icon传递的信号会带有一个整形的值, 1是表示单击右键, 2是双击, 3是单击左键, 4是用鼠标中键点击"
        if reason == 2 or reason == 3:
            pw = self.parent()
            if pw.isVisible():
                pw.hide()
            else:
                pw.show()

    def show_warning_msg(self, text):
        self.showMessage("警告", text, self.MessageIcon(QSystemTrayIcon.Warning))

    def show_info_msg(self, text):
        self.showMessage("提示", text, self.MessageIcon(QSystemTrayIcon.Information))

    def msgClickEvent(self):
        """
        Ubuntu没有生效,我的树莓派是生效的
        看来是GNOME在消息点击事件上实现
        和大家不太一致导致的

        后经测试发现GNOME在点击其他应用的消息时会触发,点击本应用的就不触发..似乎也合理?
        """
        self.showMessage("提示", "---", self.icon)

    def showYouNeedRest(self, msg="主动点击测试", level=0):
        dict_msg = {
            0: {"desc": "消息", "value": QSystemTrayIcon.NoIcon},
            1: {"desc": "提示", "value": QSystemTrayIcon.Information},
            2: {"desc": "提醒", "value": QSystemTrayIcon.Warning},
            3: {"desc": "警告", "value": QSystemTrayIcon.Critical},
        }
        vlevel = dict_msg[level]["value"]
        txt = dict_msg[level]["desc"]
        self.showMessage(txt, msg or "", self.MessageIcon(vlevel))

    def show_search_bar(self, msg="主动点击测试", level=0):
        self.parent().open_search_bar()

    def quit(self):
        # TODO 完整的退出 不过注释掉几行也能退出,蛮奇怪,先这么吧.
        self.setVisible(False)
        self.parent().close()  # qApp.quit()
        sys.exit()
