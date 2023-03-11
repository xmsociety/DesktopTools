import sys
from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import QSystemTrayIcon, QMenu

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
        self.subMenu = QMenu()
        self.showAction = QAction("测试休息提醒消息",
                                  self,
                                  triggered=self.showYouNeedRest)
        self.quitAction = QAction("退出", self, triggered=self.quit)

        self.subMenu.addAction(self.showAction)
        self.menuMain.addMenu(self.subMenu, )

        self.menuMain.addAction(self.quitAction)
        self.subMenu.setTitle("测试菜单")
        self.setContextMenu(self.menuMain)

    def initConnect(self):
        #把鼠标点击图标的信号和槽连接
        self.activated.connect(self.iconClicked)

        #把鼠标点击弹出消息的信号和槽连接
        self.messageClicked.connect(self.msgClickEvent)

        #设置图标
        self.setIcon(QIcon("harry_potter.ico"))
        self.icon = self.MessageIcon(QSystemTrayIcon.MessageIcon.NoIcon)

    def iconClicked(self, reason):
        "鼠标点击icon传递的信号会带有一个整形的值, 1是表示单击右键, 2是双击, 3是单击左键, 4是用鼠标中键点击"
        if reason == 2 or reason == 3:
            pw = self.parent()
            if pw.isVisible():
                pw.hide()
            else:
                pw.show()

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
            0: {
                "desc": "消息",
                "value": QSystemTrayIcon.NoIcon
            },
            1: {
                "desc": "提示",
                "value": QSystemTrayIcon.Information
            },
            2: {
                "desc": "提醒",
                "value": QSystemTrayIcon.Warning
            },
            3: {
                "desc": "警告",
                "value": QSystemTrayIcon.Critical
            },
        }
        vlevel = dict_msg[level]["value"]
        txt = dict_msg[level]["desc"]
        self.showMessage(txt, msg, self.MessageIcon(vlevel))

    def quit(self):
        # TODO 完整的退出 不过注释掉几行也能退出,蛮奇怪,先这么吧.
        self.setVisible(False)
        self.parent().exit()    # qApp.quit()
        sys.exit()
