import sys
import threading
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QTableWidgetItem, QApplication, QMessageBox
from PyQt5 import QtCore, QtWidgets

from ui.layout.UI_TaskPage import Ui_TaskPage
from SQL.dbFunction import *
class TaskPage(QtWidgets.QWidget,Ui_TaskPage):

    #定义信号，用于传递检测数量和单双面检测
    detectionCountAndTypeChanged = pyqtSignal(int, str)
    # 定义一个信号，传递所有选中项的信息
    itemDetailsChanged = pyqtSignal(dict)
    switchToPage = pyqtSignal(int)  # 用于主界面切换页面的信号
    def __init__(self):
        super(TaskPage, self).__init__()
        self.setupUi(self)  # 从UI_TaskPage.py中加载UI定义

        self.confirm_Button.clicked.connect(self.onPushButtonClicked)
        self.delete_Button.clicked.connect(self.onDeleteButtonClicked)

        # 设置选中行为为整行选中
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        # 确保只有单行可以被选中
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        # 调整列宽以自适应内容
        self.tableWidget.resizeColumnsToContents()
        # 调整列宽以占满整个表格
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

    def handleTaskCompletion(self, task_key):
        rows = self.tableWidget.rowCount()
        for row in range(rows):
            task_key_item = self.tableWidget.item(row, self.tableWidget.columnCount() - 1)  # 假设最后一列是"任务Key值"
            if task_key_item and task_key_item.text() == task_key:
                # 如果找到匹配的任务Key值，更新"是否完成"字段
                completion_item = QtWidgets.QTableWidgetItem("已完成")
                completion_item.setTextAlignment(QtCore.Qt.AlignCenter)  # 居中对齐文本
                self.tableWidget.setItem(row, self.tableWidget.columnCount() - 2, completion_item)  # 假设倒数第二列是"是否完成"
                break  # 如果task_key是唯一的，找到匹配项后可以直接退出循环
    def select_button(self):
        return self.select_Button
    def onPushButtonClicked(self):
        # 获取表格中选中行的“检测数量”
        selected_indexes = self.tableWidget.selectionModel().selectedRows()
        if selected_indexes:
            # 假设倒数第二列的列索引，这里需要您根据实际列数修改
            last_column_index = self.tableWidget.columnCount() - 2
            # 获取选中行的最后一列的项
            completion_status_item = self.tableWidget.item(selected_indexes[0].row(), last_column_index)
            # 检查是否完成字段的值
            if completion_status_item and completion_status_item.text() == "已完成":
                # 如果任务已完成，弹出提示
                QMessageBox.information(self, "任务状态", "当前选中的任务已完成，请选中其他任务")
                return  # 退出函数，不继续执行后面的代码
           # 获取所有列的内容
            row_data = {}
            for column in range(self.tableWidget.columnCount()):
                item = self.tableWidget.item(selected_indexes[0].row(), column)
                header = self.tableWidget.horizontalHeaderItem(column).text()  # 获取表头文本
                row_data[header] = item.text() if item else ""
            # 假设“检测数量”是第6列，索引从0开始
            detection_count_index = selected_indexes[0].sibling(selected_indexes[0].row(), 5)
            detection_count = int(self.tableWidget.itemFromIndex(detection_count_index).text())
            # 假设“识别类型”字段是第7列，索引从0开始，即列索引为6
            detection_type_index = selected_indexes[0].sibling(selected_indexes[0].row(), 6)
            detection_type = self.tableWidget.itemFromIndex(detection_type_index).text()

            # 发射信号以通知 MainWindow 切换到第二页
            self.switchToPage.emit(1)  # 页面索引从0开始，第三页的索引是2

            # 发射包含所有信息的信号
            self.itemDetailsChanged.emit(row_data)
            # 发射带有两个参数的信号
            self.detectionCountAndTypeChanged.emit(detection_count, detection_type)

    def onDeleteButtonClicked(self):
        # 获取当前选中的行
        selected_indexes = self.tableWidget.selectionModel().selectedRows()
        if not selected_indexes:
            QMessageBox.warning(self, '选择错误', '请先选择要删除的任务。')
            return

        # 确定选中的行号
        row = selected_indexes[0].row()

        # 从表中获取任务Key值
        task_key = self.tableWidget.item(row, 8)
        if task_key is None:
            QMessageBox.warning(self, '选择错误', '无法找到任务Key值。')
            return

        task_key = task_key.text()
        # 检查状态是否为“已完成”
        status_item = self.tableWidget.item(row, self.tableWidget.columnCount() - 2)  # 倒数第二列
        if status_item and status_item.text() == "已完成":
            # 如果状态为“已完成”，则只在表中删除该行，不从数据库中删除
            self.tableWidget.removeRow(row)
            QMessageBox.information(self, '操作成功', '所选任务已成功删除。')
            return  # 直接返回，不执行数据库删除操作
        # 弹出确认框
        reply = QMessageBox.question(self, '确认删除', '是否确认删除当前选中的任务？',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        # 如果用户选择“Yes”，则执行删除操作
        if reply == QMessageBox.Yes:
            connection = None
            # 从数据库中删除任务
            try:
                connection = dbConnect()
                cursor = connection.cursor()

                delete_query = "DELETE FROM TaskInformation WHERE TASK_KEY = ?"
                cursor.execute(delete_query, (task_key,))

                connection.commit()
                # 删除成功后，关闭游标和连接
                cursor.close()
                # 从表中删除选中的行
                self.tableWidget.removeRow(row)

                QMessageBox.information(self, '操作成功', '所选任务已成功删除。')

            except Exception as e:
                QMessageBox.warning(self, '数据库错误', f'无法删除任务。错误信息：{e}')
            finally:
                if connection is not None:
                    connection.close()

    def addTask(self, task_data):
        # 限制显示的行数为10
        while self.tableWidget.rowCount() > 10:
            # 从最旧的一行开始检查（即第一行）
            for rowIndex in range(self.tableWidget.rowCount()):
                # 获取每一行的最后一个字段内容
                # 假设状态是最后一列，使用columnCount() - 1来定位最后一列
                statusItem = self.tableWidget.item(rowIndex, self.tableWidget.columnCount() - 2)
                if statusItem and statusItem.text() == "已完成":
                    # 如果倒数第二个字段内容为“已完成”，则删除该行
                    self.tableWidget.removeRow(rowIndex)
                    break  # 退出循环，因为我们已经找到并删除了一行，需要重新检查行数是否符合要求
            else:
                # 如果所有行都被检查过，且没有找到状态为“已完成”的行，则退出循环
                # 这意味着没有更多状态为“已完成”的行可以删除
                break

        row_position = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row_position)  # 插入新行

        # 设置行高
        self.tableWidget.setRowHeight(row_position, 100)  # 示例行高为100
        # 根据字段顺序添加数据到表格中
        col_order = ['生产线', '任务标识符', '产品名称', '批号', '物料类型', '检测数量', '识别类型','是否完成','任务Key值']
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