import sys


from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
from PyQt5.QtGui import QIcon

from ui.layout.UI_ModelMainPage import Ui_ModelMainPage
from ui.impl.ModelManagePage import ModelManagePage
from ui.impl.TrainPage import TrainPage
from ui.impl.DataCollectPage import DataCollectPage

class ModelMainPage(QWidget, Ui_ModelMainPage):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # 主页面背景 title logo
        self.setWindowTitle('药品三期信息模型训练')
        # 设置窗口图标
        self.setWindowIcon(QIcon('ui/pic/logo.ico'))
        # 创建分页面
        self.modelmanage_page=ModelManagePage()
        self.train_page=TrainPage()
        self.datacollect_page=DataCollectPage()

        self.pages = [self.modelmanage_page, self.train_page,self.datacollect_page]

        for i in self.pages:
            self.stackedWidget.addWidget(i)
        # 连接按钮
        self.pushButton_1.clicked.connect(self.showDataCollectPage)
        self.pushButton_2.clicked.connect(self.showTrainPage)
        self.pushButton_3.clicked.connect(self.showModelManage)

    def showModelManage(self):
        self.stackedWidget.setCurrentWidget(self.modelmanage_page)

    def showTrainPage(self):
        self.stackedWidget.setCurrentWidget(self.train_page)

    def showDataCollectPage(self):
        self.stackedWidget.setCurrentWidget(self.datacollect_page)

    def closeEvent(self, event):
        # 检查 DataCollectPage 实例中是否有 labelThread 属性，并且它是否在运行
        if hasattr(self.datacollect_page, 'labelThread') and self.datacollect_page.labelThread.is_running():
            # 如果 labelThread 存在并且正在运行，显示提醒框
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setWindowTitle("提醒")
            msgBox.setText("请先关闭数据标注软件。")
            msgBox.addButton("确认", QMessageBox.AcceptRole)
            msgBox.exec_()
            event.ignore()  # 忽略关闭事件，不关闭主窗口
        else:
            # 如果 labelThread 不存在或不在运行，关闭程序
            event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mywindow = ModelMainPage()
    mywindow.showMaximized()
    sys.exit(app.exec_())