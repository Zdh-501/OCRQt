# 导入必要的库
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QLineEdit, QPushButton, QVBoxLayout, QLabel, QApplication, QWidget, QTableWidget, \
    QMessageBox
import pyodbc

from SQL.dbFunction import *

# 假设这是您的登录界面类
class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super(LoginDialog, self).__init__(parent)
        # 调整对话框大小
        self.resize(350, 200)  # 或者您可以使用更具体的尺寸
        # 移除问号按钮
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setWindowTitle('用户校验')
        self.username = QLineEdit(self)
        self.password = QLineEdit(self)
        self.password.setEchoMode(QLineEdit.Password)
        self.loginButton = QPushButton("确认", self)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("用户名（CWID）:"))
        layout.addWidget(self.username)
        layout.addWidget(QLabel("密码:"))
        layout.addWidget(self.password)
        layout.addWidget(self.loginButton)

        self.loginButton.clicked.connect(self.handleLogin)

    def handleLogin(self):
        cwid = self.username.text()
        password = self.password.text()
        connection = dbConnect()  # 假设这是您连接数据库的函数
        cursor = connection.cursor()

        # 查询用户是否存在且账号是否激活
        cursor.execute("SELECT Username, Permission FROM dbo.Users WHERE CWID = ? AND Password = ? AND IsActive = 1", (cwid, password))
        result = cursor.fetchone()

        if result:
            self.username = cwid  # 保存 CWID
            self.user_name = result[0]  # 保存用户名
            self.permission = result[1]  # 保存权限
            self.accept()  # 登录成功
        else:
            QMessageBox.warning(self, 'Error', '用户名或密码错误，或账户失效')

