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
class MainWindow(QWidget, Ui_MainPage):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # 主页面背景 title logo
        self.setWindowTitle('药品三期信息识别')

        # 设置窗口图标
        self.setWindowIcon(QIcon('ui/pic/logo.ico'))
        #todo 要添加登录界面，并更新当前显示用户

        #todo 创建分页面
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
        # 连接信号和槽任务界面模型修改
        #todo 添加检查当前用户权限
        self.task_page.select_Button.clicked.connect(self.on_select_button_clicked)
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

    def on_select_button_clicked(self):
        # 弹出配置对话框并更新 PicturePage2 实例
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