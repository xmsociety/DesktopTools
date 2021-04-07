import operator

from PySide2.QtCore import QThread, Signal, Qt, QAbstractTableModel, SIGNAL
from PySide2.QtWidgets import QDialog, QPushButton, QMessageBox, QHBoxLayout, QVBoxLayout, QWidget, QTableView
from PySide2.QtCharts import QtCharts

from data_alchemy import inputs


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
    """对QDialog类重写，实现一些功能"""
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
        table_model = MyTableModel(self, data_list, ["name", "count"])
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
            data.append((item.name, item.count))
        self.initTable(data)
        return data

    def initUI(self):
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
            # TODO 显示个表情包吧
            return None

    def closeEvent(self, event):
        """
        重写closeEvent方法，实现dialog窗体关闭时执行一些代码
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


class ThreadCounter(QThread):
    def __init__(self, screen):
        super().__init__()
        self.show_dialog(screen)

    def show_dialog(self, screen):
        dlg = CounterDialog(screen)
        dlg.setWindowTitle("Input Counter")
        dlg.setWindowModality(Qt.ApplicationModal)
        dlg.exec_()
