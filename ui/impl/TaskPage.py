import sys

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QTableWidgetItem, QApplication

from ui.layout.UI_TaskPage import Ui_TaskPage
from PyQt5 import QtCore, QtWidgets

class TaskPage(QtWidgets.QWidget,Ui_TaskPage):
    detectionCountChanged = pyqtSignal(int)  # 定义一个新信号
    # 定义一个信号，传递所有选中项的信息
    itemDetailsChanged = pyqtSignal(dict)
    switchToPage = pyqtSignal(int)  # 用于主界面切换页面的信号
    def __init__(self):
        super(TaskPage, self).__init__()
        self.setupUi(self)  # 从UI_TaskPage.py中加载UI定义

        # 假设您的按钮叫做 pushButton
        self.pushButton.clicked.connect(self.onPushButtonClicked)


        # 设置选中行为为整行选中
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        # 确保只有单行可以被选中
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        # 调整列宽以自适应内容
        self.tableWidget.resizeColumnsToContents()
        # 调整列宽以占满整个表格
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        # 添加数据
        self.addTask({
            "任务序号": 9,
            "批号": "CY32403",
            "物料类型": "小盒",
            "产品物料名称": "复方酮康唑发用洗剂15+0.25毫克50毫升成品（Rx）",
            "生产日期": "2023/11/24",
            "有效期至": "2025/11/23",
            "产线": "支装三线",
            "检测数量": 8
        })
        tasks = [
            {"任务序号": 4, "批号": "CY32404", "物料类型": "小盒","产品物料名称": "复方","生产日期": "2023/11/22","有效期至": "2025/11/24","产线": "支装二线","检测数量": 5},
            {"任务序号": 5, "批号": "CY32405", "物料类型": "小盒","产品物料名称": "复方","生产日期": "2023/10/22","有效期至": "2025/10/24","产线": "支装四线","检测数量": 10},
            {"任务序号": 2, "批号": "CY32406", "物料类型": "小盒","产品物料名称": "复方","生产日期": "2023/12/22","有效期至": "2025/12/24","产线": "支装五线","检测数量": 7},
            # 更多任务字典
        ]
        for task in tasks:
            self.addTask(task)

    def onPushButtonClicked(self):
        # 获取表格中选中行的“检测数量”
        selected_indexes = self.tableWidget.selectionModel().selectedRows()
        if selected_indexes:
            # 获取所有列的内容
            row_data = {}
            for column in range(self.tableWidget.columnCount()-1):
                item = self.tableWidget.item(selected_indexes[0].row(), column)
                header = self.tableWidget.horizontalHeaderItem(column).text()  # 获取表头文本
                row_data[header] = item.text() if item else ""

            # 发射包含所有信息的信号
            self.itemDetailsChanged.emit(row_data)
            # 假设“检测数量”是第8列，索引从0开始
            detection_count_index = selected_indexes[0].sibling(selected_indexes[0].row(), 7)
            detection_count = int(self.tableWidget.itemFromIndex(detection_count_index).text())
            self.detectionCountChanged.emit(detection_count)
            # 发射信号以通知 MainWindow 切换到第三页
            self.switchToPage.emit(2)  # 页面索引从0开始，第三页的索引是2
    def addTask(self, task_data):
        row_position = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row_position)  # 插入新行

        # 根据字段顺序添加数据到表格中
        col_order = ['任务序号', '批号', '物料类型', '产品物料名称', '生产日期', '有效期至', '产线', '检测数量']
        for col, field in enumerate(col_order):
            if field == '检测数量':
                # 对于数值字段，使用数值进行设置
                item = QTableWidgetItem()
                item.setData(QtCore.Qt.DisplayRole, int(task_data[field]))
            else:
                # 其他非数值字段，使用字符串
                item = QTableWidgetItem(str(task_data[field]))

            item.setTextAlignment(QtCore.Qt.AlignCenter)  # 设置文本居中
            self.tableWidget.setItem(row_position, col, item)


# if __name__ == '__main__':
# app = QApplication(sys.argv)
# mainWindow = TaskPage()
# mainWindow.show()
# app.exec_()