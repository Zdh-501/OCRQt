import sys
from datetime import datetime
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QPushButton, QHBoxLayout, QWidget, QTableWidgetItem, QApplication

from ui.layout.UI_UsersPage import Ui_UsersPage
from SQL.dbFunction import *
from ui.impl.UserManagementDialog import *
#todo 管理失效时间
class UsersPage(QtWidgets.QWidget,Ui_UsersPage):
    def __init__(self):
        super(UsersPage, self).__init__()
        self.setupUi(self)  # 从UI_TaskPage.py中加载UI定义
        self.loadUsersData()

    def set_user_info(self, cwid, name, permission):
        self.user_cwid = cwid
        self.user_name = name
        self.user_permission = permission
    def loadUsersData(self):
        connection = dbConnect()
        cursor = connection.cursor()
        cursor.execute("SELECT CWID, UserName, Permission, IsActive, LastLoginTime, ExpiryTime FROM Users")

        # 首先收集需要更新的记录
        records_to_update = []
        for row_data in cursor:
            is_active = row_data[3]
            expiry_time = row_data[5]
            if is_active and expiry_time and datetime.now() > expiry_time:
                records_to_update.append(row_data[0])  # 收集需要更新的CWID

        # 更新数据库中的用户状态
        for cwid in records_to_update:
            with connection.cursor() as update_cursor:
                update_cursor.execute("UPDATE Users SET IsActive = ? WHERE CWID = ?", (False, cwid))
            connection.commit()

        # 重新查询数据以更新界面显示
        cursor.execute("SELECT CWID, UserName, Permission, IsActive, LastLoginTime, ExpiryTime FROM Users")
        self.setupTableWidget(cursor)  # 将表格设置和数据填充放到一个单独的函数
        connection.close()

    def setupTableWidget(self, cursor):
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(
            ['CWID', '用户名称', '权限', '状态', '最近登录时间', '失效时间', '操作'])
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        for row_number, row_data in enumerate(cursor):
            self.tableWidget.insertRow(row_number)
            row_height = 60
            self.tableWidget.setRowHeight(row_number, row_height)
            for column_number, data in enumerate(row_data):
                if column_number == 2:
                    data = "管理员" if data == '1' else "操作员" if data == '2' else "未知权限"
                elif column_number == 3:
                    data = "激活" if data else "失效"
                cell_item = QTableWidgetItem(str(data))
                cell_item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.tableWidget.setItem(row_number, column_number, cell_item)
            self.addOperationButtons(row_number, row_data[0])

        header = self.tableWidget.horizontalHeader()
        for i in range(7):
            header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)

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
        self.tableWidget.setCellWidget(row_number, 6, container)


    def changeUserPassword(self, cwid):
        #todo 处理“修改密码”按钮点击事件
        print(f"Changing password for user with CWID: {cwid}")

    def manageUser(self, cwid):
        dialog = UserManagementDialog(cwid, self)
        if dialog.exec_():
            # 可以在这里重新加载用户数据来更新UI
            self.loadUsersData()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mywindow = UsersPage()
    mywindow.showMaximized()
    sys.exit(app.exec_())