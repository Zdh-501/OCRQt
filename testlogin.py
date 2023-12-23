import sys
import bcrypt
import pymysql
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Login and Registration')

        layout = QVBoxLayout(self)

        # 用户名输入
        self.usernameLabel = QLabel('Username:', self)
        layout.addWidget(self.usernameLabel)

        self.usernameInput = QLineEdit(self)
        layout.addWidget(self.usernameInput)

        # 密码输入
        self.passwordLabel = QLabel('Password:', self)
        layout.addWidget(self.passwordLabel)

        self.passwordInput = QLineEdit(self)
        self.passwordInput.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.passwordInput)

        # 登录按钮
        self.loginButton = QPushButton('Login', self)
        self.loginButton.clicked.connect(self.check_login)
        layout.addWidget(self.loginButton)

        # 注册按钮
        self.registerButton = QPushButton('Register', self)
        self.registerButton.clicked.connect(self.register)
        layout.addWidget(self.registerButton)

    def check_login(self):
        username = self.usernameInput.text()
        password = self.passwordInput.text()

        connection = pymysql.connect(host='lcoalhost', user='root', password='abcd123456',
                                     db='test')

        try:
            with connection.cursor() as cursor:
                sql = "SELECT password_hash FROM users WHERE username=%s"
                cursor.execute(sql, (username,))
                result = cursor.fetchone()
                if result and bcrypt.checkpw(password.encode('utf-8'), result[0].encode('utf-8')):
                    QMessageBox.information(self, 'Success', 'You have logged in.')
                    #todo 登录成功，跳转到主界面
                else:
                    print('Invalid username or password')
                    QMessageBox.warning(self, 'Error', 'Invalid username or password')
        finally:
            connection.close()

    def register(self):
        # 这里添加打开注册窗口的逻辑
        self.registrationWindow = RegistrationWindow()
        self.registrationWindow.show()

class RegistrationWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Register New User')

        layout = QVBoxLayout(self)

        self.usernameLabel = QLabel('Username:', self)
        layout.addWidget(self.usernameLabel)

        self.usernameInput = QLineEdit(self)
        layout.addWidget(self.usernameInput)

        self.passwordLabel = QLabel('Password:', self)
        layout.addWidget(self.passwordLabel)

        self.passwordInput = QLineEdit(self)
        self.passwordInput.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.passwordInput)

        self.emailLabel = QLabel('Email:', self)
        layout.addWidget(self.emailLabel)

        self.emailInput = QLineEdit(self)
        layout.addWidget(self.emailInput)

        self.submitButton = QPushButton('Submit', self)
        self.submitButton.clicked.connect(self.submit_registration)
        layout.addWidget(self.submitButton)

    def submit_registration(self):
        username = self.usernameInput.text()
        password = self.passwordInput.text()
        email = self.emailInput.text()

        # 简单的输入验证
        if not username or not password or not email:
            QMessageBox.warning(self, 'Error', 'All fields are required')
            return

        # 对密码进行哈希处理
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        connection = pymysql.connect(host='localhost', user='root', password='abcd123456',
                                     db='test')

        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO users (username, password_hash, email) VALUES (%s, %s, %s)"
                cursor.execute(sql, (username, hashed, email))
                connection.commit()
            QMessageBox.information(self, 'Success', 'Registration successful')
        except pymysql.MySQLError as e:
            QMessageBox.warning(self, 'Error', f'Database error: {e}')
        finally:
            connection.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())
