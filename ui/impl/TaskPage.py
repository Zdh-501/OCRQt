import sys

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QTableWidgetItem, QApplication

from ui.layout.UI_TaskPage import Ui_TaskPage
from PyQt5 import QtCore, QtWidgets

class TaskPage(QtWidgets.QWidget,Ui_TaskPage):

    #定义信号，用于传递检测数量和单双面检测
    detectionCountAndTypeChanged = pyqtSignal(int, str)
    # 定义一个信号，传递所有选中项的信息
    itemDetailsChanged = pyqtSignal(dict)
    switchToPage = pyqtSignal(int)  # 用于主界面切换页面的信号
    def __init__(self):
        super(TaskPage, self).__init__()
        self.setupUi(self)  # 从UI_TaskPage.py中加载UI定义

        # 假设您的按钮叫做 pushButton
        self.confirm_Button.clicked.connect(self.onPushButtonClicked)



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
            "批号": "CY32403",
            "物料类型": "小盒",
            "产品名称": "复方酮康唑发用洗剂15+0.25毫克50毫升成品（Rx）",
            "任务标识符": "包盒IPC 抽查[1.1]",
            "生产线": "支装一线",
            "检测数量": 8,
            "单/双面检测": "单面",
            "是否完成": "未完成"
        })
        tasks = [
            { "批号": "CY32404", "物料类型": "中盒","产品名称": "复方酮康唑发用洗剂15+0.25毫克5毫升成品（缅甸）","任务标识符": "包盒IPC 抽查[1.2]","生产线": "支装一线","检测数量": 5 ,"单/双面检测": "双面","是否完成": "未完成"},
            {"批号": "CY32405", "物料类型": "内包材","产品名称": "复方酮康唑软膏 10+0.5 毫克 5g 成品（缅甸）","任务标识符": "包盒IPC 抽查[1.3]","生产线": "支装一线","检测数量": 10, "单/双面检测": "单面","是否完成": "未完成"},
            { "批号": "CY32406", "物料类型": "小盒","产品名称": "复方","任务标识符": "包盒IPC 抽查[1.4]","生产线": "支装一线","检测数量": 7, "单/双面检测": "单面","是否完成": "已完成"},
            # 更多任务字典
        ]
        for task in tasks:
            self.addTask(task)

    def select_button(self):
        return self.select_Button
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
            # 此处需要修改 假设“检测数量”是第6列，索引从0开始
            detection_count_index = selected_indexes[0].sibling(selected_indexes[0].row(), 5)
            detection_count = int(self.tableWidget.itemFromIndex(detection_count_index).text())
            # 假设“单双面检测”字段是第7列，索引从0开始，即列索引为6
            detection_type_index = selected_indexes[0].sibling(selected_indexes[0].row(), 6)
            detection_type = self.tableWidget.itemFromIndex(detection_type_index).text()
            # 发射带有两个参数的信号
            self.detectionCountAndTypeChanged.emit(detection_count, detection_type)
            #todo 需要添加产品名称信息，用于设置相机参数

            # 发射信号以通知 MainWindow 切换到第二页
            self.switchToPage.emit(1)  # 页面索引从0开始，第三页的索引是2
    def addTask(self, task_data):
        #todo 从数据库中读取
        # 限制显示的行数为10
        while self.tableWidget.rowCount() >= 10:
            self.tableWidget.removeRow(0)  # 删除最旧的一行

        row_position = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row_position)  # 插入新行

        # 设置行高
        self.tableWidget.setRowHeight(row_position, 100)  # 示例行高为100
        # 根据字段顺序添加数据到表格中
        col_order = ['生产线', '任务标识符', '产品名称', '批号', '物料类型', '检测数量', '单/双面检测','是否完成']
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = TaskPage()
    mainWindow.show()
    app.exec_()