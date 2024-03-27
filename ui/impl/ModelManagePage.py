import sys
from datetime import datetime
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QTableWidgetItem, QApplication, QHeaderView, QWidget, QHBoxLayout, QPushButton, QMessageBox
from PyQt5 import QtCore, QtWidgets

from ui.layout.UI_ModelManagePage import Ui_ModelManagePage
from SQL.dbFunction import *

class ModelManagePage(QtWidgets.QWidget,Ui_ModelManagePage):

    def __init__(self):
        super(ModelManagePage, self).__init__()
        self.setupUi(self)  # 加载UI定义
        # 设置除了状态列之外的所有列为根据表格宽度均匀分配
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 设置表格列标题
        columns = ['模型ID', '模型名称','预训练模型', 'CWID', '用户名称', '开始训练时间', '状态', '操作']
        self.tableWidget.setColumnCount(len(columns))
        for index, column_name in enumerate(columns):
            self.tableWidget.setHorizontalHeaderItem(index, QtWidgets.QTableWidgetItem(column_name))
        #self.load_models()  # 调用加载模型数据的方法
        self.load_models_from_database()

    def load_models_from_database(self):
        # 连接数据库
        connection = dbConnect()
        cursor = connection.cursor()

        # SQL 查询模型信息，确保包含ModelID, Remarks, 和 StoragePath
        query = "SELECT ModelID, ModelName, PretrainedModelName, CWID, UserName, TrainingStartTime, Status, Remarks, StoragePath FROM ModelInformation"
        try:
            cursor.execute(query)
            models_data = cursor.fetchall()  # 获取所有查询结果
            self.populate_table(models_data)
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            cursor.close()
            connection.close()
    def load_models(self):
        # 假定有一些模型数据需要加载
        models_data = [
            # 示例数据
            {'模型名称': '模型2','CWID':'root','用户名称':'root','开始训练时间':'2024/1/29/11:00', '预训练模型': '模型1', '备注': '训练某药品的模型', '状态': '训练中'},
            {'模型名称': '模型3', 'CWID':'root','用户名称':'root','开始训练时间':'2024/1/29/11:00','预训练模型': '模型1', '备注': '训练某药品的模型', '状态': '已完成'}
            # 添加更多模型数据...
        ]
        #self.populate_table(models_data)

    def populate_table(self, models_data):
        self.tableWidget.setColumnCount(8)  # 现在是7个可见数据列和1个操作列
        # 保持原有的行高和字体设置不变
        row_height = 100
        font = QFont()
        font.setPointSize(10)

        self.tableWidget.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeToContents)
        self.tableWidget.setRowCount(len(models_data))  # 根据数据设置行数

        for row_index, row_data in enumerate(models_data):
            self.tableWidget.setRowHeight(row_index, row_height)
            for col_index, item in enumerate(row_data[:-2]):  # 排除最后两项(即Remarks和StoragePath)
                # 检查TrainingStartTime是否是datetime对象
                if col_index == 5:  # 假设TrainingStartTime是第六个字段
                    if isinstance(item, datetime):
                        item = item.strftime("%Y/%m/%d %H:%M:%S")
                table_item = QTableWidgetItem(str(item))
                # 保持原有的字体设置
                table_item.setFont(font)
                table_item.setTextAlignment(Qt.AlignCenter)
                table_item.setFlags(table_item.flags() & ~Qt.ItemIsEditable)
                self.tableWidget.setItem(row_index, col_index, table_item)

            # 传递ModelID到操作按钮的添加方法中
            self.add_action_buttons(row_index, row_data[0], row_data[-2], row_data[-1])
    def add_action_buttons(self, row, model_id ,remarks, storage_path):
        # 创建包含按钮的QWidget
        widget = QWidget()
        layout = QHBoxLayout(widget)

        # 删除按钮
        btn_delete = QPushButton('删除')
        btn_delete.clicked.connect(lambda: self.delete_model(model_id))
        layout.addWidget(btn_delete)

        # 查看备注按钮
        btn_view_remarks = QPushButton('查看备注')
        btn_view_remarks.clicked.connect(lambda: self.show_popup(remarks))
        layout.addWidget(btn_view_remarks)

        # 查看路径按钮
        btn_view_path = QPushButton('查看路径')
        btn_view_path.clicked.connect(lambda: self.show_popup(storage_path))
        layout.addWidget(btn_view_path)

        # 设置布局并将其添加到表格中
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignCenter)
        widget.setLayout(layout)
        self.tableWidget.setCellWidget(row, 7, widget)  # 假设操作列是第8列

    def delete_model(self, model_id):
        # 首先确认用户想要删除模型
        reply = QMessageBox.question(self, '确认删除',
                                     "你确定要删除这个模型吗?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            try:
                # 连接数据库
                connection = dbConnect()
                cursor = connection.cursor()

                # 使用参数化的查询来防止SQL注入
                query = "DELETE FROM ModelInformation WHERE ModelID = ?"
                cursor.execute(query, (model_id,))

                # 提交数据库操作
                connection.commit()

                # 从表格视图中移除对应的行
                # 这里假设每行的第一列是ModelID
                for i in range(self.tableWidget.rowCount()):
                    if self.tableWidget.item(i, 0).text() == str(model_id):
                        self.tableWidget.removeRow(i)
                        break

                print(f"模型 {model_id} 已从数据库中删除。")
            except Exception as e:
                QMessageBox.warning(self, '删除失败', f"删除模型失败: {e}")
            finally:
                cursor.close()
                connection.close()

    def show_popup(self, message):
        QMessageBox.information(self, "信息", message)






        # 实现保存路径的逻辑
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     mainWindow = ModelManagePage()
#     mainWindow.show()
#     app.exec_()