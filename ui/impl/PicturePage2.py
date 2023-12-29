import sys

import pymysql
import requests
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QLabel, QMessageBox, QMenu, QWidget
from PyQt5.QtGui import QPixmap, QStandardItemModel, QStandardItem, QImage
from PyQt5.QtCore import Qt, pyqtSignal, QTimer, QModelIndex, QEvent, Q_ARG, QBuffer, QIODevice
from pyqt5_plugins.examplebutton import QtWidgets
import re
from PIL import Image
from mphdcpy import mphdc
import cv2 as cv
import ctypes as ct
import time
from paddleocr import PaddleOCR
from io import BytesIO
from ui.layout.UI_PicturePage2 import Ui_PicturePage2  # 假设UI类名为Ui_PicturePage
from ui.impl.TaskDialog import TaskDialog
from ui.impl.myThread import *
from SQL.dbFunction import *

class PicturePage2(QtWidgets.QWidget, Ui_PicturePage2):
    def __init__(self):
        super(PicturePage2, self).__init__()
        self.setupUi(self)

        # 初始化 PaddleOCR 配置
        self.det_model_dir = r"D:/Paddle/ResNet50_1220"
        self.rec_model_dir = "D:/Paddle/rec"
        self.use_angle_cls = True
        self.det_db_unclip_ratio = 2.8
        self.lang = 'en'

        # 创建 PaddleOCR 实例
        self.initialize_ocr()

        self.current_label_index = 0
        self.currentTaskNumber = None  # 添加一个变量来存储当前选中的任务序号
        self.isCameraStarted = False  # 相机是否已启动的标志
        self.captured_images = []  # 用于存储捕获的图像

        self.startDetectButton.clicked.connect(self.onStartDetectClicked)
        self.takePictureButton.clicked.connect(self.start_camera_view)
        self.skipButton.clicked.connect(self.take_photo_and_skip)

        current_username = 'root'
        workstation_number = self.get_workstation_number(current_username)
        if workstation_number is not None:
            self.textBrowser_2.setText(f"生产工位: {workstation_number}")
        else:
            self.textBrowser_2.setText("无")
    def init_camera(self):
        self.camera = mphdc.CreateCamera(ct.c_int(mphdc.LogMediaType.Off.value), ct.c_int(1))
        mphdc.UpdateCameraList(self.camera)

        camera_info = mphdc.GetCameraInfo(self.camera, 0)
        mphdc.OpenCamera(self.camera, camera_info)

        #self.camera_worker.image_captured.connect(self.display_image_on_label)

        # 创建CameraWorker线程
        self.camera_worker = CameraWorker(self.camera)

        # 连接 image_captured 信号到 display_image_on_label 方法
        self.camera_worker.image_captured.connect(self.display_image_on_label)


        self.camera_worker.start()

    def initialize_ocr(self):
        # 使用当前配置创建 PaddleOCR 实例
        self.ocr = PaddleOCR(det_model_dir=self.det_model_dir,
                             rec_model_dir=self.rec_model_dir,
                             use_angle_cls=self.use_angle_cls,
                             det_db_unclip_ratio=self.det_db_unclip_ratio,
                             lang=self.lang)

    def update_ocr_config(self, config):
        # 更新配置
        self.det_model_dir = config.get('det_model_dir', self.det_model_dir)
        self.rec_model_dir = config.get('rec_model_dir', self.rec_model_dir)
        self.use_angle_cls = config.get('use_angle_cls', self.use_angle_cls)
        self.det_db_unclip_ratio = config.get('det_db_unclip_ratio', self.det_db_unclip_ratio)
        self.lang = config.get('lang', self.lang)

        # 重新初始化 PaddleOCR 实例
        self.initialize_ocr()
    def updateTextBrowser(self, item_details):
        # 将字典转换为字符串
        details_str = '\n'.join(f"{key}: {value}" for key, value in item_details.items())

        # 设置 textBrowser_3 的字体
        font = self.textBrowser_3.font()  # 获取当前字体
        font.setPointSize(12)  # 设置字体大小为 12，或者您希望的其他大小
        self.textBrowser_3.setFont(font)

        # 更新 textBrowser_3 的内容
        self.textBrowser_3.setText(details_str)
    def setLabelsAndPages(self, count):
        self.progressBar.setSegmentCount(count)
        # 清除当前的所有 pages 和 labels
        while self.stackedWidget.count() > 0:
            widget_to_remove = self.stackedWidget.widget(0)
            self.stackedWidget.removeWidget(widget_to_remove)
            widget_to_remove.deleteLater()
        self.labels = []
        self.pages = []
        for i in range(count):
            # 创建 label
            label = QtWidgets.QLabel(f"Label {i + 1}")
            label.setAlignment(QtCore.Qt.AlignCenter)  # 设置 label 文字居中显示
            self.labels.append(label)
            # 创建 page
            page = QtWidgets.QWidget()
            layout = QtWidgets.QVBoxLayout()  # 创建 QVBoxLayout
            layout.addWidget(label)  # 将 label 添加到 QVBoxLayout
            page.setLayout(layout)  # 设置 page 的布局
            self.pages.append(page)

            # 将 page 添加到 QStackedWidget
            self.stackedWidget.addWidget(page)

        # 如果需要，可以在此处设置 QStackedWidget 显示第一页
        self.stackedWidget.setCurrentIndex(0)
        #进度条等分
        self.progressBar.setMaximum(count)
        self.progressBar.setMinimum(0)
        self.progressBar.clickedValue.connect(self.onProgressBarClicked)

    def onProgressBarClicked(self, value):
        # 计算点击的是第几份
        whichPart = value

        # 设置当前索引为点击的部分
        self.stackedWidget.setCurrentIndex(whichPart)

        # 更新进度条的值（可选，如果您希望点击进度条后进度条也反映当前页面）
        self.progressBar.setValue(whichPart+1)





    def onStartDetectClicked(self):

        self.captured_images.clear()  # 清空存储的图像列表
        self.showTaskDialog()


    def showTaskDialog(self):
        task_name = "是否确定执行任务"
        dialog = TaskDialog(task_name)
        result = dialog.exec_()
        if result:
            print("开始检测任务")
            # 可以选择在这里关闭相机，或者保持打开状态
            if self.camera_worker.isRunning():
                self.camera_worker.stop()
                self.camera_worker.wait()
            self.detectTask()  # 调用检测任务函数
        else:
            print("任务取消")

    def detectTask(self):
        self.thread = OcrThread(self.captured_images)  # 使用捕获的图像
        self.thread.finished.connect(self.onOcrFinished)
        self.thread.start()

    def onOcrFinished(self, results):
        # 处理OCR结果
        for label_index, result in results:
            print(f"在 label_{label_index + 1} 的检测结果：", result)
        # 可以在这里更新UI等
    def display_image_on_label(self, image_np):
        print("Displaying image on label")
        # 同时将图像存储在列表中
        self.captured_images.append(image_np)
        # 显示图像在当前标签上
        q_image = QImage(image_np.data, image_np.shape[1], image_np.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)
        self.labels[self.current_label_index].setPixmap(
            pixmap.scaled(self.labels[self.current_label_index].size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def closeEvent(self, event):
        # 确保相机线程被正确关闭
        if self.camera_worker.isRunning():
            self.camera_worker.stop()
            self.camera_worker.wait()
        event.accept()

    def clearLabels(self):
        for label in self.labels:
            label.clear()  # 清空标签上的图片

    def start_camera_view(self):

        # 检查相机是否已经初始化
        if not hasattr(self, 'camera'):
            # 初始化相机
            self.init_camera()
            # 启动相机工作线程
            self.camera_worker.start()

        # 更新 UI 状态
        if self.current_label_index < len(self.labels):
            # 切换到当前标签对应的页面
            self.stackedWidget.setCurrentIndex(self.current_label_index)


    def capture_image(self):
        # 从相机捕获图像，并显示在当前标签上
        state = mphdc.GetCamearState(self.camera)
        if state == mphdc.DeviceStateType.StandBy:
            res, data = mphdc.SanpCamera(self.camera, 2000)
            if res:
                imgs, n, _ = mphdc.Nppc_Create(data)
                if n > 0:
                    self.display_image_on_label(imgs[0])
                else:
                    print("未捕获到图像")
            else:
                print("拍摄失败")
    def take_photo_and_skip(self):
        #todo
        # 捕获当前图像
        self.capture_image()
        # 移动到下一个标签
        self.current_label_index += 1
        self.progressBar.setValue(self.current_label_index)
        # 检查是否已到达标签列表的末尾
        if self.current_label_index < len(self.labels):
            # 更新当前显示的标签和页面
            self.stackedWidget.setCurrentIndex(self.current_label_index)
            # 如果不是最后一个标签，重启相机预览线程
            self.camera_worker.start()
        else:
            # 如果是最后一个标签，则重置索引
            self.current_label_index = 0
            # 可以选择在这里关闭相机，或者保持打开状态
            if self.camera_worker.isRunning():
                self.camera_worker.stop()
                self.camera_worker.wait()

    def take_photos1(self):
        filenames, _ = QFileDialog.getOpenFileNames(self, "Select Images", "", "Image Files (*.png *.jpg *.jpeg *.bmp)")
        if not filenames:
            return

        for i, filename in enumerate(filenames[:8]):
            pixmap = QPixmap(filename)
            self.labels[i].setPixmap(pixmap.scaled(self.labels[i].size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.labels[i].setScaledContents(True)
            # 如果 label 显示了图片，将对应的 pushButton 颜色设置为绿色
            if not pixmap.isNull():
                getattr(self, f'pushButton_{i + 1}').setStyleSheet('background-color: green;')

    def get_workstation_number(self, username):
        # 用您的数据库连接信息替换以下内容
        connection = dbConnect()

        try:
            with connection.cursor() as cursor:
                sql = "SELECT number FROM dbo.users WHERE username = ?"
                cursor.execute(sql, (username,))
                result = cursor.fetchone()
                return result['number'] if result else None
        finally:
            connection.close()


#创建应用实例和窗口，然后运行
# app = QApplication(sys.argv)
# window = PicturePage2()
# window.showMaximized()
# sys.exit(app.exec_())
