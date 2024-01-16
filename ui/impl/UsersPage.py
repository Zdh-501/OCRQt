import sys

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QPushButton, QHBoxLayout, QWidget, QTableWidgetItem, QApplication

from ui.layout.UI_UsersPage import Ui_UsersPage
from SQL.dbFunction import *

class UsersPage(QtWidgets.QWidget,Ui_UsersPage):
    def __init__(self):
        super(UsersPage, self).__init__()
        self.setupUi(self)  # 从UI_TaskPage.py中加载UI定义
        self.loadUsersData()

    def loadUsersData(self):
        connection = dbConnect()
        cursor = connection.cursor()
        cursor.execute("SELECT CWID, Permission, IsActive FROM Users")

        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(4)  # 有四个字段：用户名, 权限, 状态, 操作
        self.tableWidget.setHorizontalHeaderLabels(['用户名', '权限', '状态', '操作'])
        # 设置行为整行选中
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        # 设置表格为只读
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        for row_number, row_data in enumerate(cursor):
            self.tableWidget.insertRow(row_number)
            # 设置行高
            row_height = 60  # 将行高设置为60像素
            self.tableWidget.setRowHeight(row_number, row_height)  # 设置行高
            for column_number, data in enumerate(row_data):
                if column_number == 1:  # 权限字段
                    # 根据字符串内容转换权限描述
                    data = "管理员" if data == '1' else "操作员" if data == '2' else "未知权限"
                elif column_number == 2:  # 状态字段
                    data = "激活" if data else "未激活"  # 假设IsActive是布尔类型
                # 创建单元格项并设置居中对齐
                cell_item = QTableWidgetItem(str(data))
                cell_item.setTextAlignment(QtCore.Qt.AlignCenter)  # 设置文本居中
                self.tableWidget.setItem(row_number, column_number, cell_item)

            self.addOperationButtons(row_number, row_data[0])

        # 设置列宽等宽并占满表格
        header = self.tableWidget.horizontalHeader()
        for i in range(4):
            header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
        connection.close()

    def addOperationButtons(self, row_number, cwid):
        # 创建“管理”和“修改密码”按钮
        manage_button = QPushButton('管理')
        change_password_button = QPushButton('修改密码')

        # 为按钮设置点击事件处理函数
        manage_button.clicked.connect(lambda: self.manageUser(cwid))
        change_password_button.clicked.connect(lambda: self.changeUserPassword(cwid))

        # 创建一个水平布局来放置按钮
        layout = QHBoxLayout()
        layout.addWidget(manage_button)
        layout.addWidget(change_password_button)
        layout.setContentsMargins(0, 0, 0, 0)  # 移除布局边距

        # 创建一个容器小部件来放置布局
        container = QWidget()
        container.setLayout(layout)

        # 将容器小部件放置到表格中的“操作”列
        self.tableWidget.setCellWidget(row_number, 3, container)

    def manageUser(self, cwid):
        # 处理“管理”按钮点击事件
        print(f"Managing user with CWID: {cwid}")

    def changeUserPassword(self, cwid):
        # 处理“修改密码”按钮点击事件
        print(f"Changing password for user with CWID: {cwid}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mywindow = UsersPage()
    mywindow.showMaximized()
    sys.exit(app.exec_())