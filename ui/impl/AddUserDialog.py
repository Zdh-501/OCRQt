# AddUserDialog.py
from PyQt5 import QtWidgets, QtCore, QtGui
from datetime import datetime, timedelta
from SQL.dbFunction import dbConnect
from PyQt5.QtCore import Qt
import re
class AddUserDialog(QtWidgets.QDialog):
    # 定义一个信号，当用户添加成功时发射
    userAdded = QtCore.pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('新增用户')
        self.resize(400, 300)
        self.setupUi()

    def setupUi(self):
        layout = QtWidgets.QVBoxLayout(self)
        font = QtGui.QFont()
        font.setPointSize(14)  # 设置字体大小为14，与 UserManagementDialog 保持一致
        # 移除问号按钮
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        # 创建并设置输入字段
        self.cwidLineEdit = QtWidgets.QLineEdit(self)
        self.cwidLineEdit.setFont(font)  # 应用字体
        self.nameLineEdit = QtWidgets.QLineEdit(self)
        self.nameLineEdit.setFont(font)  # 应用字体
        self.passwordLineEdit = QtWidgets.QLineEdit(self)
        self.passwordLineEdit.setFont(font)  # 应用字体
        self.passwordLineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.permissionComboBox = QtWidgets.QComboBox(self)
        self.permissionComboBox.setFont(font)  # 应用字体
        self.permissionComboBox.addItems(['管理员', '操作员'])
        self.permissionComboBox.setStyleSheet("QComboBox { font-size: 14pt; }")  # 设置样式

        self.isActiveCheckBox = QtWidgets.QCheckBox('激活', self)
        self.isActiveCheckBox.setFont(font)  # 应用字体
        self.expiryTimeSpinBox = QtWidgets.QSpinBox(self)
        self.expiryTimeSpinBox.setFont(font)  # 应用字体
        self.expiryTimeSpinBox.setRange(1, 60)
        self.expiryTimeSpinBox.setStyleSheet("QSpinBox { font-size: 14pt; }")  # 设置样式

        # 创建保存按钮并设置字体
        saveButton = QtWidgets.QPushButton('保存', self)
        saveButton.setFont(font)  # 应用字体
        saveButton.clicked.connect(self.saveUser)

        # 添加输入字段到布局
        layout.addWidget(QtWidgets.QLabel('CWID:'))
        layout.addWidget(self.cwidLineEdit)
        layout.addWidget(QtWidgets.QLabel('用户名称:'))
        layout.addWidget(self.nameLineEdit)
        layout.addWidget(QtWidgets.QLabel('密码:'))
        layout.addWidget(self.passwordLineEdit)
        layout.addWidget(QtWidgets.QLabel('权限:'))
        layout.addWidget(self.permissionComboBox)
        layout.addWidget(self.isActiveCheckBox)
        layout.addWidget(QtWidgets.QLabel('失效时间（月）:'))
        layout.addWidget(self.expiryTimeSpinBox)
        layout.addWidget(saveButton)

    def validate_password(self, password):
        # 检查密码是否至少有8个字符
        if len(password) < 8:
            return False

        # 计算密码中包含的字符类别数
        categories = [
            r"[A-Z]",  # 大写字母
            r"[a-z]",  # 小写字母
            r"[0-9]",  # 数字
            r"[!@#$%^&*(),.?\":{}|<>]"  # 特殊字符
        ]

        category_count = 0
        for pattern in categories:
            if re.search(pattern, password):
                category_count += 1

        # 检查是否至少包含三种字符类别
        return category_count >= 3
    def saveUser(self):
        # 获取输入值
        cwid = self.cwidLineEdit.text()
        name = self.nameLineEdit.text()
        password = self.passwordLineEdit.text()
        permission_text = self.permissionComboBox.currentText()
        permission = '1' if permission_text == '管理员' else '2'  # 将权限转换为相应的数字
        is_active = self.isActiveCheckBox.isChecked()
        expiry_months = self.expiryTimeSpinBox.value()
        expiry_time = datetime.now() + timedelta(days=expiry_months * 30)  # 转换为日期
        # 验证密码复杂性
        if not self.validate_password(password):
            QtWidgets.QMessageBox.warning(self, '错误', '密码不符合安全要求。')
            return  # 如果密码不符合要求，停止执行并返回
        # 连接数据库并保存新用户
        try:
            connection = dbConnect()
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO Users (CWID, UserName, Password, Permission, IsActive, ExpiryTime)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (cwid, name, password, permission, is_active, expiry_time))
            connection.commit()
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, '错误', f'添加用户时发生错误：{e}')
        finally:
            cursor.close()
            connection.close()
        self.userAdded.emit()
        self.accept()  # 关闭对话框
        # 如果用户添加成功，发射信号


