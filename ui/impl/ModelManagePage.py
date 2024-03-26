import sys

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QTableWidgetItem, QApplication, QHeaderView, QWidget, QHBoxLayout, QPushButton
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
        columns = ['模型名称', '预训练模型', 'CWID', '用户名称', '开始训练时间', '备注', '状态', '操作']
        self.tableWidget.setColumnCount(len(columns))
        for index, column_name in enumerate(columns):
            self.tableWidget.setHorizontalHeaderItem(index, QtWidgets.QTableWidgetItem(column_name))
        #self.load_models()  # 调用加载模型数据的方法
        self.load_models_from_database()

    def load_models_from_database(self):
        # 连接数据库
        connection = dbConnect()
        cursor = connection.cursor()

        # SQL 查询模型信息
        query = "SELECT ModelName, PretrainedModelName, CWID, UserName, TrainingStartTime, Remarks, Status FROM ModelInformation"
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
        self.tableWidget.setColumnCount(8)  # 你有7个数据列和1个操作列

        # 设置行高和字体
        row_height = 100  # 设置一个合适的行高，例如50像素
        font = QFont()
        font.setPointSize(10)  # 设置一个合适的字体大小，例如10点

        self.tableWidget.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeToContents)

        self.tableWidget.setRowCount(len(models_data))  # 根据数据设置行数
        for row_index, row_data in enumerate(models_data):
            self.tableWidget.setRowHeight(row_index, row_height)
            # 假设数据库查询结果与列的顺序是匹配的
            for col_index, item in enumerate(row_data):
                # 格式化时间
                if col_index == 4:  # 假设第五个字段是时间
                    item = item.strftime("%Y/%m/%d %H:%M:%S") if item else ""
                table_item = QTableWidgetItem(str(item))
                table_item.setFont(font)  # 设置字体
                table_item.setTextAlignment(Qt.AlignCenter)  # 设置文本居中
                # 设置为不可编辑
                table_item.setFlags(table_item.flags() & ~Qt.ItemIsEditable)

                self.tableWidget.setItem(row_index, col_index, table_item)
            self.add_action_buttons(row_index)  # 为每行添加操作按钮

    def add_action_buttons(self, row):
        # 创建包含按钮的QWidget
        widget = QWidget()
        layout = QHBoxLayout(widget)

        # 创建字体对象并设置字体大小
        font = QFont()
        font.setPointSize(10)  # 这里设置按钮的字体大小为10点
        # 创建删除按钮
        btn_delete = QPushButton('删除', self)
        btn_delete.setFont(font)  # 应用字体设置
        btn_delete.clicked.connect(self.create_delete_function(row))
        layout.addWidget(btn_delete)

        # 创建再次训练按钮
        btn_retrain = QPushButton('重新训练', self)
        btn_retrain.setFont(font)  # 应用字体设置
        btn_retrain.clicked.connect(self.create_retrain_function(row))
        layout.addWidget(btn_retrain)

        # 创建保存路径按钮
        btn_check_path = QPushButton('查看路径')
        btn_check_path.setFont(font)  # 应用字体设置
        btn_check_path.clicked.connect(self.create_check_path_function(row))
        layout.addWidget(btn_check_path)

        # 设置布局
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(QtCore.Qt.AlignCenter)
        widget.setLayout(layout)

        # 将QWidget设置为表格中的项
        self.tableWidget.setCellWidget(row, 7, widget)

    def delete_model(self, row):
        # 删除模型的函数
        print(f"删除第{row}行的模型")
        # 在这里实现删除模型的逻辑

    def retrain_model(self, row):
        # 再次训练模型的函数
        print(f"对第{row}行的模型进行重新训练")
        # 在这里实现再次训练模型的逻辑

    def create_check_path_function(self, row):
        # 工厂函数，为每个按钮创建保存路径函数
        def check_path():
            self.check_model_path(row)

        return check_path

    def create_delete_function(self, row):
        def delete():
            self.delete_model(row)

        return delete

    def create_retrain_function(self, row):
        def retrain():
            self.retrain_model(row)

        return retrain

    def check_model_path(self, row):
        # 保存路径的函数
        print(f"查看第{row}行的模型路径")
        # 实现保存路径的逻辑
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     mainWindow = ModelManagePage()
#     mainWindow.show()
#     app.exec_()