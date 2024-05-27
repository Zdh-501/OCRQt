from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QMessageBox, QLineEdit
from PyQt5.QtCore import Qt
from SQL.dbFunction import dbConnect
from datetime import datetime, timedelta
import re

class ChangePasswordDialog(QtWidgets.QDialog):
    def __init__(self, cwid, parent=None):
        super().__init__(parent)
        self.cwid = cwid
        self.initUI()

    def initUI(self):
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.resize(400, 120)
        self.setWindowTitle('修改密码')

        self.layout = QtWidgets.QVBoxLayout(self)

        font = QtGui.QFont()
        font.setPointSize(14)

        self.passwordLabel = QtWidgets.QLabel('新密码:')
        self.passwordLabel.setFont(font)
        self.passwordEdit = QLineEdit()
        self.passwordEdit.setFont(font)
        self.passwordEdit.setFixedSize(400, 50)
        self.passwordEdit.setEchoMode(QLineEdit.Password)

        self.confirmPasswordLabel = QtWidgets.QLabel('确认密码:')
        self.confirmPasswordLabel.setFont(font)
        self.confirmPasswordEdit = QLineEdit()
        self.confirmPasswordEdit.setFont(font)
        self.confirmPasswordEdit.setFixedSize(400, 50)
        self.confirmPasswordEdit.setEchoMode(QLineEdit.Password)

        self.saveButton = QtWidgets.QPushButton('保存')
        self.saveButton.setFont(font)
        self.saveButton.clicked.connect(self.saveChanges)

        self.layout.addWidget(self.passwordLabel)
        self.layout.addWidget(self.passwordEdit)
        self.layout.addWidget(self.confirmPasswordLabel)
        self.layout.addWidget(self.confirmPasswordEdit)
        self.layout.addWidget(self.saveButton)

    def saveChanges(self):
        password = self.passwordEdit.text()
        confirmPassword = self.confirmPasswordEdit.text()

        if not self.isValidPassword(password):
            QMessageBox.warning(self, '错误', '密码不符合安全要求。')
            return

        if password != confirmPassword:
            QMessageBox.warning(self, '错误', '两次输入的密码不一致！')
            return
        expiry_time = datetime.now() + timedelta(days=49)  # 49天
        connection = dbConnect()
        cursor = connection.cursor()

        try:
            cursor.execute("""
                UPDATE Users
                SET Password = ?, ExpiryTime = ?
                WHERE CWID = ?
            """, (password, expiry_time,self.cwid))
            connection.commit()
            QMessageBox.information(self, '成功', '密码修改成功！')
            self.accept()
        except Exception as e:
            QMessageBox.warning(self, '错误', f'更新数据库时发生错误：{e}')
        finally:
            cursor.close()
            connection.close()

    def isValidPassword(self, password):
        # 检查长度
        if len(password) < 8:
            return False

        # 检查是否包含 CWID
        if self.cwid in password:
            return False

        # 检查是否包含至少三种类型的字符
        count = 0
        if re.search(r'[A-Z]', password):  # 大写字母
            count += 1
        if re.search(r'[a-z]', password):  # 小写字母
            count += 1
        if re.search(r'[0-9]', password):  # 数字
            count += 1
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):  # 特殊字符
            count += 1

        return count >= 3