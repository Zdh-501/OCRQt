import sys
from datetime import datetime
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox

from PyQt5.QtGui import QIcon

from ui.layout.UI_MainPage import Ui_MainPage
from ui.impl.PicturePage import PicturePage
from ui.impl.RecordPage import RecordPage
from ui.impl.TaskPage import TaskPage
from ui.impl.LogPage import LogPage
from ui.impl.UsersPage import UsersPage
from ui.impl.OCRConfigDialog import *
from ui.impl.LoginDialog import LoginDialog

from SQL.dbFunction import *
class MainWindow(QWidget, Ui_MainPage):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # 主页面背景 title logo
        self.setWindowTitle('药品三期信息识别')

        # 设置窗口图标
        self.setWindowIcon(QIcon('ui/pic/logo.ico'))

        #创建分页面
        self.task_page=TaskPage()
        self.picture_page=PicturePage()
        self.picture_page.isComplete=True
        self.record_page=RecordPage()
        self.log_page=LogPage()
        self.users_page=UsersPage()

        # 连接信号和槽
        self.task_page.detectionCountAndTypeChanged.connect(self.picture_page.setLabelsAndPages)
        # 连接 TaskPage 的 itemDetailsChanged 信号到 PicturePage 的槽
        self.task_page.itemDetailsChanged.connect(self.picture_page.updateTextBrowser)
        # 连接信号和槽切换主界面
        self.task_page.switchToPage.connect(self.switchPage)
        self.log_page.flashButton.clicked.connect(self.flashErrorData)
        # 检测任务完成发送信号切换页面 备用
        #self.picture_page.Compl.connect(self.showTaskPage)

        self.pages = [self.task_page,self.picture_page,self.record_page,self.log_page,self.users_page]

        for i in self.pages:
            self.stackedWidget.addWidget(i)

        #连接按钮

        self.pushButton_1.clicked.connect(self.showTaskPage)
        self.pushButton_2.clicked.connect(self.showPicturePage)
        self.pushButton_3.clicked.connect(self.showRecordPage)
        self.pushButton_4.clicked.connect(self.showLogPage)
        self.pushButton_5.clicked.connect(self.showUsersPage)
        # pushButton_6 是退出当前用户的按钮
        self.pushButton_6.clicked.connect(self.logout_user)
        # 进入登录界面，并更新当前显示用户
        self.perform_logout()

    def show_permission_warning(self):
        QMessageBox.warning(self, '权限不足', '您没有执行该操作的权限。')
    def logout_user(self):
        # 检查任务完成状态列表是否不为空且最后一项不为True
        if self.picture_page.task_completion_status and not self.picture_page.task_completion_status[-1]:
            # 弹出提示框提醒用户任务未完成
            QMessageBox.warning(self, "任务未完成", "当前检测任务未完成，请先完成当前任务再退出用户", QMessageBox.Ok)
            # 获取当前时间
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # 错误信息
            error_message = "存在未完成任务的情况下点击了退出登录按钮"

            try:
                # 连接数据库
                connection = dbConnect()
                cursor = connection.cursor()

                # 插入错误信息到 ErrorLog 表
                insert_query = """
                                       INSERT INTO ErrorLog (OccurrenceTime, ErrorMessage ,CWID ,UserName)
                                        VALUES (?, ? ,? ,?)
                                       """
                cursor.execute(insert_query, (current_time, error_message, self.user_cwid, self.user_name))
                connection.commit()

                print("错误信息已记录到数据库")
            except pyodbc.Error as e:
                print("数据库错误: ", e)
            finally:
                # 确保无论如何都关闭数据库连接
                if connection:
                    connection.close()
            return
        # 弹出提示框询问用户是否退出
        reply = QMessageBox.question(self, '退出登录', "是否退出当前用户？", QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.perform_logout()

    def perform_logout(self):
        while True:
            # 展示登录对话框
            login_dialog = LoginDialog(self)
            login_dialog.setModal(True)  # 使登录对话框成为模态
            if login_dialog.exec_() == QDialog.Accepted:
                # 保存登录用户的信息
                self.user_cwid = login_dialog.username
                self.user_name = login_dialog.user_name
                self.user_permission = login_dialog.permission
                self.userName.setText(self.user_name)  # 更新界面以反映用户登录
                # 获取当前时间作为最后登录时间
                current_time = datetime.now()

                # 更新数据库的 LastLoginTime 字段
                try:
                    connection = dbConnect()
                    cursor = connection.cursor()
                    cursor.execute("""
                                    UPDATE Users
                                    SET LastLoginTime = ?
                                    WHERE CWID = ?
                                """, (current_time, self.user_cwid))
                    connection.commit()
                except Exception as e:
                    print(f"更新登录时间出错: {e}")
                finally:
                    cursor.close()
                    connection.close()
                # 更新分页面的用户信息
                self.picture_page.set_user_info(self.user_cwid, self.user_name, self.user_permission)
                self.users_page.set_user_info(self.user_cwid, self.user_name, self.user_permission)
                #加载用户信息
                self.users_page.loadUsersData()
                #加载错误日志
                self.loadErrorLogs()
                # 断开 select_Button 上可能存在的所有连接
                try:
                    self.task_page.select_Button.clicked.disconnect()
                    self.log_page.clearButton.clicked.disconnect()
                except TypeError:
                    # 如果之前没有连接，则会抛出 TypeError 异常，可以忽略
                    pass
                #todo 根据用户权限决定是否连接信号 错误日志界面 用户管理界面
                if self.user_permission == '1':  # 确认管理员权限
                    # 连接信号和槽任务界面模型修改
                    self.task_page.select_Button.clicked.connect(self.on_select_button_clicked)
                    # 连接清除按钮的信号
                    self.log_page.clearButton.clicked.connect(self.clearErrorLogs)
                else:
                    # 如果权限不足，禁用按钮或连接到权限警告
                    self.task_page.select_Button.clicked.connect(self.show_permission_warning)
                    self.log_page.clearButton.clicked.connect(self.show_permission_warning)

                break
            else:
                # 用户取消登录，弹出提示是否重试
                retry_reply = QMessageBox.question(self, '登录失败', "您必须登录才能继续。是否重新登录？", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
                if retry_reply == QMessageBox.No:
                    sys.exit()  # 关闭整个应用程序
                    return  # 退出 perform_logout 方法
        # 初始化时更新用户管理按钮行为
        self.users_page.updateButtonBehaviors()
    #不在LogPage中添加此函数，而在此处跟新loadError避免当前用户信息未初始化的问题
    def loadErrorLogs(self):
        # 连接到数据库
        connection = dbConnect()
        cursor = connection.cursor()

        if self.user_permission == '1':
            # 如果是管理员，查询所有数据
            cursor.execute("SELECT OccurrenceTime, CWID, UserName, ErrorMessage FROM ErrorLog")
            column_count = 4
            header_labels = ["发生时间", "CWID", "用户名称", "错误信息"]
        else:
            # 如果不是管理员，只显示与self.user_cwid相对应的数据
            query = "SELECT OccurrenceTime, ErrorMessage FROM ErrorLog WHERE CWID = ?"
            cursor.execute(query, (self.user_cwid,))
            column_count = 2
            header_labels = ["发生时间", "错误信息"]

        rows = cursor.fetchall()

        # 设置tableWidget的行数和列数
        self.log_page.tableWidget.setRowCount(len(rows))
        self.log_page.tableWidget.setColumnCount(column_count)

        # 设置列标题
        self.log_page.tableWidget.setHorizontalHeaderLabels(header_labels)
        # 设置表格头（列标题）的伸缩模式为Stretch，以使所有列均匀地占据整个表格宽度
        header = self.log_page.tableWidget.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        # 设置字体
        font = QtGui.QFont()
        font.setPointSize(13)  # 设置字体大小为13

        # 设置行高
        row_height = 50  # 将行高设置为50像素

        # 遍历并添加数据到tableWidget中
        for row_number, row_data in enumerate(rows):
            self.log_page.tableWidget.setRowHeight(row_number, row_height)  # 设置行高

            for column_number, data in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem(str(data))
                item.setFont(font)  # 设置字体
                # 设置单元格不可编辑
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                #居中显示
                if not column_number == 3:
                    item.setTextAlignment(Qt.AlignCenter)
                # 如果是第一列，设置文本居中对齐
                if column_number == 0:
                    item.setTextAlignment(Qt.AlignCenter)

                self.log_page.tableWidget.setItem(row_number, column_number, item)


        # 关闭数据库连接
        if connection:
            connection.close()
    def flashErrorData(self):
        self.loadErrorLogs()
    def clearErrorLogs(self):
        # 弹出提示框以确认操作
        reply = QMessageBox.question(self, '确认删除', '是否要删除全部错误信息？',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            # 用户确认删除
            # 连接到数据库
            connection = dbConnect()
            cursor = connection.cursor()

            # 删除ErrorLog表中的所有数据
            cursor.execute("DELETE FROM ErrorLog")

            # 提交更改
            connection.commit()



            # 关闭数据库连接
            connection.close()

    def on_select_button_clicked(self):
        # 弹出配置对话框并更新 PicturePage 实例
        dialog = OCRConfigDialog(self)
        if dialog.exec_():
            config = dialog.getConfig()
            self.picture_page.update_ocr_config(config)
    def switchPage(self, pageIndex):
        self.stackedWidget.setCurrentIndex(pageIndex)
    def showTaskPage(self):
        # 检查当前任务是否完成
        if not self.picture_page.isComplete:  # 注意这里是 not self.picture_page.isComplete
            # 如果任务未完成，询问用户是否继续
            reply = QMessageBox.question(self, '任务正在进行',
                                         "当前有任务正在进行，是否继续切换页面？",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                # 如果用户选择“是”，则允许切换页面
                self.stackedWidget.setCurrentWidget(self.task_page)
            else:
                # 如果用户选择“否”，则不进行任何操作
                pass
        else:
            # 如果任务已完成，直接切换页面
            self.stackedWidget.setCurrentWidget(self.task_page)
    def showPicturePage(self):
        self.stackedWidget.setCurrentWidget(self.picture_page)
    def showRecordPage(self):
        # 检查当前任务是否完成
        if not self.picture_page.isComplete:  # 注意这里是 not self.picture_page.isComplete
            # 如果任务未完成，询问用户是否继续
            reply = QMessageBox.question(self, '任务正在进行',
                                         "当前有任务正在进行，是否继续切换页面？",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                # 如果用户选择“是”，则允许切换页面
                self.stackedWidget.setCurrentWidget(self.record_page)
            else:
                # 如果用户选择“否”，则不进行任何操作
                pass
        else:
            # 如果任务已完成，直接切换页面
            self.stackedWidget.setCurrentWidget(self.record_page)

    def showLogPage(self):
        # 检查当前任务是否完成
        if not self.picture_page.isComplete:  # 注意这里是 not self.picture_page.isComplete
            # 如果任务未完成，询问用户是否继续
            reply = QMessageBox.question(self, '任务正在进行',
                                         "当前有任务正在进行，是否继续切换页面？",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                # 如果用户选择“是”，则允许切换页面
                self.stackedWidget.setCurrentWidget(self.log_page)
            else:
                # 如果用户选择“否”，则不进行任何操作
                pass
        else:
            # 如果任务已完成，直接切换页面
            self.stackedWidget.setCurrentWidget(self.log_page)
    def showUsersPage(self):
        # 检查当前任务是否完成
        if not self.picture_page.isComplete:  # 注意这里是 not self.picture_page.isComplete
            # 如果任务未完成，询问用户是否继续
            reply = QMessageBox.question(self, '任务正在进行',
                                         "当前有任务正在进行，是否继续切换页面？",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                # 如果用户选择“是”，则允许切换页面
                self.stackedWidget.setCurrentWidget(self.users_page)
            else:
                # 如果用户选择“否”，则不进行任何操作
                pass
        else:
            # 如果任务已完成，直接切换页面
            self.stackedWidget.setCurrentWidget(self.users_page)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mywindow = MainWindow()
    mywindow.showMaximized()
    sys.exit(app.exec_())