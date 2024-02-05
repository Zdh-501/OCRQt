from PyQt5 import QtWidgets,QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox
from datetime import datetime, timedelta

from SQL.dbFunction import *
class UserManagementDialog(QtWidgets.QDialog):
    def __init__(self, cwid, parent=None):
        super().__init__(parent)
        self.cwid = cwid
        self.initUI()


    def initUI(self):
        # 移除问号按钮
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        # 调整对话框大小
        self.resize(400, 300)  # 或者您可以使用更具体的尺寸
        self.setWindowTitle('管理用户')
        self.layout = QtWidgets.QVBoxLayout(self)

        # 设置字体
        font = QtGui.QFont()
        font.setPointSize(14)  # 设置字体大小为14
        # 状态标签和下拉框
        self.statusLabel = QtWidgets.QLabel('用户状态:')
        self.statusLabel.setFont(font)
        self.statusComboBox = QtWidgets.QComboBox()
        self.statusComboBox.addItems(['激活', '失效'])
        self.statusComboBox.setFixedSize(400, 50)
        self.statusComboBox.setStyleSheet("QComboBox { font-size: 14pt; }")

        self.expiryTimeLabel = QtWidgets.QLabel('失效时间（以月为单位）:')
        self.expiryTimeLabel.setFont(font)
        self.expiryTimeEdit = QtWidgets.QSpinBox()
        self.expiryTimeEdit.setMinimum(1)  # 至少一个月
        self.expiryTimeEdit.setMaximum(60)  # 最多五年
        # 设置固定大小或者样式
        self.expiryTimeEdit.setFixedSize(400, 50)  # 或者使用样式表
        # 设置 QSpinBox 的样式
        self.expiryTimeEdit.setStyleSheet("QSpinBox { font-size: 14pt; }")

        self.permissionLabel = QtWidgets.QLabel('用户权限:')
        self.permissionLabel.setFont(font)
        self.permissionComboBox = QtWidgets.QComboBox()
        self.permissionComboBox.addItems(['管理员', '操作员'])
        self.permissionComboBox.setFixedSize(400,50)

        # 设置 QComboBox 控件和下拉菜单项的样式
        self.permissionComboBox.setStyleSheet("""
                    QComboBox {
                        font-size: 14pt;
                    }
                    QComboBox QAbstractItemView {
                        font-size: 15pt;  # 设置下拉菜单项的字体大小
                    }
                """)
        self.saveButton = QtWidgets.QPushButton('保存')

        self.saveButton.clicked.connect(self.saveChanges)

        self.layout.addWidget(self.statusLabel)
        self.layout.addWidget(self.statusComboBox)
        self.layout.addWidget(self.expiryTimeLabel)
        self.layout.addWidget(self.expiryTimeEdit)
        self.layout.addWidget(self.permissionLabel)
        self.layout.addWidget(self.permissionComboBox)
        self.layout.addWidget(self.saveButton)

    def saveChanges(self):
        connection = dbConnect()
        cursor = connection.cursor()

        # 根据statusComboBox的值设置isActive
        is_active = True if self.statusComboBox.currentText() == '激活' else False

        # 根据expiryTimeEdit的值和当前时间计算ExpiryTime
        expiry_months = self.expiryTimeEdit.value()
        expiry_time = datetime.now() + timedelta(days=expiry_months * 30)  # 大约每月30天

        # 根据permissionComboBox的值设置Permission
        permission_value = 1 if self.permissionComboBox.currentText() == '管理员' else 2

        try:
            # 更新数据库
            cursor.execute("""
                UPDATE Users
                SET IsActive = ?, ExpiryTime = ?, Permission = ?
                WHERE CWID = ?
            """, (is_active, expiry_time, permission_value, self.cwid))
            connection.commit()

            QMessageBox.information(self, '成功', '用户信息更新成功！')
        except Exception as e:
            QMessageBox.warning(self, '错误', f'更新数据库时发生错误：{e}')
        finally:
            cursor.close()
            connection.close()

        self.accept()
