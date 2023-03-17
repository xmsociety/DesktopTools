import operator

from PySide6.QtCore import SIGNAL, QAbstractTableModel, Qt, QThread, Signal
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QMessageBox,
    QPushButton,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from data_alchemy import inputs
from logger import logger

# from PySide2.QtCharts import QtCharts # PySide6 不能这么引入


class MyTableModel(QAbstractTableModel):
    def __init__(self, parent, mylist, header, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.mylist = mylist
        self.header = header

    def rowCount(self, parent):
        return len(self.mylist)

    def columnCount(self, parent):
        return len(self.mylist[0])

    def data(self, index, role):
        if not index.isValid():
            return None
        elif role != Qt.DisplayRole:
            return None
        return self.mylist[index.row()][index.column()]

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header[col]
        return None

    def sort(self, col, order):
        """sort table by given column number col"""
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.mylist = sorted(self.mylist, key=operator.itemgetter(col))
        if order == Qt.DescendingOrder:
            self.mylist.reverse()
        self.emit(SIGNAL("layoutChanged()"))


class CounterDialog(QDialog):
    """
    显示按键统计表格
    对QDialog类重写
    实现统计键盘按键统计的功能
    """

    def __init__(self, screen=None):
        super().__init__()
        self.chat = None
        self.table_view = None
        self.screen = screen
        # self.setFixedSize()
        self.resize(int(screen.width() / 2), int(screen.height() / 2))
        self.initData()
        self.initUI()

    def initTable(self, data_list: list):
        """
        data_list = [
            ('ACETIC ACID', 117.9, 16.7, 1.049),
            ('ACETIC ANHYDRIDE', 140.1, -73.1, 1.087),
            ...
        ]
        """
        table_model = MyTableModel(
            self, data_list, ["name", "count", "vk", "update_time"]
        )
        table_view = QTableView()
        table_view.setModel(table_model)
        # set column width to fit contents (set font first!)
        table_view.resizeColumnsToContents()
        # enable sorting
        table_view.setSortingEnabled(True)
        self.table_view = table_view
        return 1

    def initData(self):
        # line_series = QtCharts.QLineSeries()
        # axisX = QtCharts.QBarCategoryAxis()

        # for num, item in enumerate(inputs.iter_count_on()):
        #     axisX.append(str(item.name))
        #     line_series.append(num, item.count)
        #     print(f"{item.name}: ({num}, {item.count})")

        # chat = QtCharts.QChart()
        # chat.addSeries(line_series)
        # chat.addAxis(axisX, Qt.AlignBottom)
        # line_series.attachAxis(axisX)
        # self.chat = chat
        data = []
        for item in inputs.iter_count_on():
            data.append((item.name, item.count, item.vk, str(item.update_time)))
        self.initTable(data)
        return data

    def initUI(self):
        self.setWindowTitle("Input Counter")

        self.hbox = QHBoxLayout()
        self.vbox = QVBoxLayout()

        self.b1 = QPushButton("save")
        if self.table_view:
            # central_widget = QWidget()
            # self.chartView = QtCharts.QChartView(self.chat, central_widget)
            # self.vbox.addWidget(self.chartView)
            self.vbox.addWidget(self.table_view)
            self.hbox.addWidget(self.b1)
            self.vbox.addLayout(self.hbox)

            self.setLayout(self.vbox)
            self.show()
        else:
            logger.error("self.initTable(data) 需在 initUI前调用.")

    def closeEvent(self, event):
        """
        重写closeEvent方法, 实现dialog窗体关闭时执行一些代码
        :param event: close()触发的事件
        :return: None
        """
        return None
        # 暂时没有啥需要在关闭时处理...
        # reply = QMessageBox.question(self, '本程序', "是否要退出程序？", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        # if reply == QMessageBox.Yes:
        #     event.accept()
        # else:
        #     event.ignore()


def show_count(screen):
    table = CounterDialog(screen)
    table.setWindowModality(Qt.ApplicationModal)
    table.exec_()


"""
此方法作废,会在关闭窗口后无法正常结束线程引发主程序崩溃错误

class ThreadCounter(QThread):
    # def click_1(self, button): 从main.py中移到这儿了. 代码备份,以后有地方用到再搬
    #     # button.setEnabled(False)
    #     # pyside开启窗口貌似自己实现了多线程,不用特意使用...
    #     # 反而还会引起关闭窗口无法正常结束线程错误
    #     # 所以此方法作废,看来是单一界面有处理事件时才需特殊开启
    #     self.thread_1 = ThreadCounter(self.screen)
    #     # self.thread_1._signal.connect(lambda: self.enableButton(button))
    #     self.thread_1.start()    # 开始线程

    def __init__(self, screen):
        super().__init__()
        self.show_dialog(screen)

    def show_dialog(self, screen):
        dlg = CounterDialog(screen)
        dlg.setWindowModality(Qt.ApplicationModal)
        dlg.exec_()
"""
