import sys


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
        # todo 需要重新补充 权限检测逻辑 比如log日志待修改、用户管理
        self.perform_logout()
    def show_permission_warning(self):
        QMessageBox.warning(self, '权限不足', '您没有执行该操作的权限。')
    def logout_user(self):
        # 检查任务完成状态列表是否不为空且最后一项不为True
        if self.picture_page.task_completion_status and not self.picture_page.task_completion_status[-1]:
            # 弹出提示框提醒用户任务未完成
            QMessageBox.warning(self, "任务未完成", "当前检测任务未完成，请先完成当前任务再退出用户", QMessageBox.Ok)
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
                # 断开 select_Button 上可能存在的所有连接
                try:
                    self.task_page.select_Button.clicked.disconnect()
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