import sys

from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
from PyQt5.QtGui import QIcon

from ui.layout.UI_ModelMainPage import Ui_ModelMainPage
from ui.impl.ModelManagePage import ModelManagePage
from ui.impl.TrainPage import TrainPage
from ui.impl.DataCollectPage import DataCollectPage
from ui.impl.LoginDialog import *
class ModelMainPage(QWidget, Ui_ModelMainPage):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # 主页面背景 title logo
        self.setWindowTitle('药品三期信息模型训练')
        # 设置窗口图标
        self.setWindowIcon(QIcon('ui/pic/logo.ico'))
        # 调用登录逻辑
        self.perform_login()
        # 创建分页面
        self.modelmanage_page=ModelManagePage()
        self.train_page=TrainPage(self.user_cwid,self.user_cwid)
        self.datacollect_page=DataCollectPage()

        self.pages = [self.modelmanage_page, self.train_page,self.datacollect_page]

        for i in self.pages:
            self.stackedWidget.addWidget(i)
        # 连接按钮
        self.pushButton_1.clicked.connect(self.showDataCollectPage)
        self.pushButton_2.clicked.connect(self.showTrainPage)
        self.pushButton_3.clicked.connect(self.showModelManage)
        self.pushButton_4.clicked.connect(self.logout_user)
        # 连接信号到槽
        # 连接训练页面的信号到相应的槽
        self.train_page.trainStrat.connect(self.on_training_started)
        self.train_page.trainStrat.connect(self.modelmanage_page.load_models_from_database)
        self.train_page.trainingFinished.connect(self.on_training_finished)
        self.train_in_progress = False  # 添加一个标记，初始设置为 False
    def on_training_finished(self, success, training_start_time):
        self.train_in_progress = False  # 更新训练状态标记
        if success:
            # 更新数据库中的模型状态为“已完成”
            connection = dbConnect()
            cursor = connection.cursor()
            try:
                update_query = """
                    UPDATE ModelInformation
                    SET Status = '已完成'
                    WHERE TrainingStartTime = ?
                """
                cursor.execute(update_query, (training_start_time,))
                connection.commit()
            except Exception as e:
                QMessageBox.warning(self, '更新失败', f"更新模型状态失败: {e}")
            finally:
                cursor.close()
                connection.close()
            # 重新加载模型信息
            self.modelmanage_page.load_models_from_database()


    def on_training_started(self):
        # 设置一个标记，表示训练正在进行
        self.train_in_progress = True
    def logout_user(self):
        # 弹出提示框询问用户是否退出
        reply = QMessageBox.question(self, '退出登录', "是否退出当前用户？", QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.perform_login()
    def perform_login(self):
        while True:
            login_dialog = LoginDialog(self)
            login_dialog.setModal(True)
            if login_dialog.exec_() == QDialog.Accepted:
                # 保存用户信息
                self.user_cwid = login_dialog.username
                self.user_name = login_dialog.user_name
                self.user_permission = login_dialog.permission


                # 检查用户权限，只允许管理员登录
                if self.user_permission != '1':
                    QMessageBox.warning(self, "权限不足", "只有管理员可以登录此页面。请使用管理员账户登录。")
                    continue  # 继续显示登录对话框

                # 更新界面以反映用户登录，如设置欢迎信息等
                self.userName.setText(self.user_name) # 假设有一个标签显示用户名

                # 这里可以添加其他登录成功后需要执行的代码
                # 比如更新界面元素的访问权限等

                break
            else:
                # 用户取消登录，询问是否重新登录或退出程序
                reply = QMessageBox.question(self, '登录失败', "您必须登录才能继续。是否重新登录？",
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
                if reply == QMessageBox.No:
                    sys.exit()  # 退出程序
    def showModelManage(self):
        self.stackedWidget.setCurrentWidget(self.modelmanage_page)

    def showTrainPage(self):
        self.stackedWidget.setCurrentWidget(self.train_page)

    def showDataCollectPage(self):
        self.stackedWidget.setCurrentWidget(self.datacollect_page)

    # def closeEvent(self, event):
    #     # 检查 DataCollectPage 实例中是否有 labelThread 属性，并且它是否在运行
    #     if hasattr(self.datacollect_page, 'labelThread') and self.datacollect_page.labelThread.is_running():
    #         # 如果 labelThread 存在并且正在运行，显示提醒框
    #         msgBox = QMessageBox()
    #         msgBox.setIcon(QMessageBox.Information)
    #         msgBox.setWindowTitle("提醒")
    #         msgBox.setText("请先关闭数据标注软件。")
    #         msgBox.addButton("确认", QMessageBox.AcceptRole)
    #         msgBox.exec_()
    #         event.ignore()  # 忽略关闭事件，不关闭主窗口
    #     else:
    #         # 如果 labelThread 不存在或不在运行，关闭程序
    #         event.accept()

    def closeEvent(self, event):
        if self.train_in_progress:
            # 如果训练正在进行，显示提示消息并忽略关闭事件
            QMessageBox.warning(self, '操作不允许', '当前模型正在训练，请勿关闭软件。')
            event.ignore()
        elif hasattr(self.datacollect_page, 'labelThread') and self.datacollect_page.labelThread.is_running():
            # 如果 DataCollectPage 实例中的 labelThread 存在且正在运行，显示提醒框
            QMessageBox.warning(self, '提醒', '请先关闭数据标注软件。')
            event.ignore()  # 忽略关闭事件，不关闭主窗口
        else:
            # 如果没有正在进行的训练和数据标注，可以正常关闭
            event.accept()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mywindow = ModelMainPage()
    mywindow.showMaximized()
    sys.exit(app.exec_())