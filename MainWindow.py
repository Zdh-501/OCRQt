import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QBrush, QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QStackedLayout, QWidget, QSplashScreen, QFileDialog, QMainWindow
from pyqt5_plugins.examplebutton import QtWidgets
from pyqt5_plugins.examplebuttonplugin import QtGui
from PyQt5.QtGui import QIcon

from ui.layout.UI_MainPage import Ui_MainPage
from ui.impl.PicturePage import PicturePage
from ui.impl.PicturePage2 import PicturePage2
from ui.impl.RecordPage import RecordPage
from ui.impl.TaskPage import TaskPage
from ui.impl.OCRConfigDialog import *
class MainWindow(QWidget, Ui_MainPage):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # 主页面背景 title logo
        self.setWindowTitle('药品三期信息识别')

        # 设置窗口图标
        self.setWindowIcon(QIcon('ui/pic/logo.ico'))

        #todo 创建分页面
        self.task_page=TaskPage()
        self.picture_page=PicturePage()
        self.picture2_page=PicturePage2()
        self.record_page=RecordPage()
        # 连接信号和槽
        self.task_page.detectionCountChanged.connect(self.picture2_page.setLabelsAndPages)
        # 连接 TaskPage 的 itemDetailsChanged 信号到 PicturePage2 的槽
        self.task_page.itemDetailsChanged.connect(self.picture2_page.updateTextBrowser)
        # 连接信号和槽切换主界面
        self.task_page.switchToPage.connect(self.switchPage)
        # 连接信号和槽任务界面模型修改
        self.task_page.select_Button.clicked.connect(self.on_select_button_clicked)

        self.pages = [self.task_page,self.picture_page,self.picture2_page,self.record_page]

        for i in self.pages:
            self.stackedWidget.addWidget(i)

        #连接按钮

        self.pushButton_1.clicked.connect(self.showTaskPage)
        self.pushButton_2.clicked.connect(self.showTestPage)
        self.pushButton_3.clicked.connect(self.showPicturePage)
        self.pushButton_4.clicked.connect(self.showRecordPage)

    def on_select_button_clicked(self):
        # 弹出配置对话框并更新 PicturePage2 实例
        dialog = OCRConfigDialog(self)
        if dialog.exec_():
            config = dialog.getConfig()
            self.picture2_page.update_ocr_config(config)
    def switchPage(self, pageIndex):
        self.stackedWidget.setCurrentIndex(pageIndex)
    def showTaskPage(self):
        self.stackedWidget.setCurrentWidget(self.task_page)
    def showPicturePage(self):
        self.stackedWidget.setCurrentWidget(self.picture2_page)

    def showTestPage(self):
        self.stackedWidget.setCurrentWidget(self.picture_page)

    def showRecordPage(self):
        self.stackedWidget.setCurrentWidget(self.record_page)





if __name__ == '__main__':
    app = QApplication(sys.argv)
    mywindow = MainWindow()
    mywindow.showMaximized()
    sys.exit(app.exec_())