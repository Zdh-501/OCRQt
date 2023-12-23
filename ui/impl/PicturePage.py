import sys

import pymysql
import requests
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
from ui.layout.UI_PicturePage import Ui_PicturePage  # 假设UI类名为Ui_PicturePage
from ui.impl.TaskDialog import TaskDialog
from ui.impl.myThread import *
from SQL.dbFunction import *

class PicturePage(QtWidgets.QWidget, Ui_PicturePage):
    def __init__(self):
        super(PicturePage, self).__init__()
        self.setupUi(self)
    #     # 创建 PaddleOCR 实例
    #     self.ocr = PaddleOCR(det_model_dir=r"D:/Paddle/ResNet50_1220",
    #                     rec_model_dir="D:/Paddle/rec",
    #                     use_angle_cls=True,
    #                     det_db_unclip_ratio=2.8,
    #                     lang='en')
    #
    #     self.current_label_index = 0
    #     self.currentTaskNumber = None  # 添加一个变量来存储当前选中的任务序号
    #     self.pollingStarted = False    # 是否开始轮询检查接收任务
    #     self.isCameraStarted = False  # 相机是否已启动的标志
    #     self.captured_images = []  # 用于存储捕获的图像
    #
    #     self.startDetectButton.clicked.connect(self.onStartDetectClicked)
    #     self.takePictureButton.clicked.connect(self.start_camera_view)
    #     self.skipButton.clicked.connect(self.take_photo_and_skip)
    #     self.fetchButton.clicked.connect(self.onStartPolling)
    #
    #     #任务列表
    #     self.taskModel = QStandardItemModel(self.taskListView)
    #     self.taskListView.setModel(self.taskModel)
    #     self.taskListView.clicked.connect(self.onTaskClicked)
    #     self.taskListView.setContextMenuPolicy(Qt.CustomContextMenu)
    #     self.taskListView.customContextMenuRequested.connect(self.openMenu)
    #
    #
    #
    #     # 测试 调用 processTaskData 来加载模拟数据
    #     self.processTaskData()
    #     self.connectButtons()
    #
    #
    #     self.labels = [self.label_1, self.label_2, self.label_3, self.label_4,
    #                    self.label_5, self.label_6, self.label_7, self.label_8]
    #
    #     self.pages = [self.page_1,self.page_2,self.page_3,self.page_4,self.page_5,
    #                   self.page_6,self.page_7,self.page_8,self.page_9]
    #     current_username = 'root'
    #     workstation_number = self.get_workstation_number(current_username)
    #     if workstation_number is not None:
    #         self.textBrowser_2.setText(f"生产工位: {workstation_number}")
    #     else:
    #         self.textBrowser_2.setText("无")
    #
    #
    #
    # def init_camera(self):
    #     self.camera = mphdc.CreateCamera(ct.c_int(mphdc.LogMediaType.Off.value), ct.c_int(1))
    #     mphdc.UpdateCameraList(self.camera)
    #
    #     camera_info = mphdc.GetCameraInfo(self.camera, 0)
    #     mphdc.OpenCamera(self.camera, camera_info)
    #     # 创建CameraWorker线程
    #     self.camera_worker = CameraWorker(self.camera)
    #     self.camera_worker.image_captured.connect(self.display_image_on_label)
    #     self.camera_worker.start()
    #
    #
    #
    # def connectButtons(self):
    #     self.pushButton_1.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
    #     self.pushButton_2.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
    #     self.pushButton_3.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))
    #     self.pushButton_4.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(3))
    #     self.pushButton_5.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(4))
    #     self.pushButton_6.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(5))
    #     self.pushButton_7.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(6))
    #     self.pushButton_8.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(7))
    #     self.pushButton_9.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(8))
    # def openMenu(self, position):
    #     menu = QMenu()
    #
    #     deleteAction = menu.addAction("删除")
    #     action = menu.exec_(self.taskListView.viewport().mapToGlobal(position))
    #
    #     if action == deleteAction:
    #         self.confirmDelete(position)
    #
    # def confirmDelete(self, position):
    #     index = self.taskListView.indexAt(position)
    #     if index.isValid():
    #         task_info = index.data()
    #         reply = QMessageBox.question(self, '确认', f'是否确认删除\n{task_info}',
    #                                      QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
    #
    #         if reply == QMessageBox.Yes:
    #             self.taskModel.removeRow(index.row())
    # def onStartPolling(self):
    #     api_url = self.apiInput.text().strip()
    #     if api_url and not self.pollingStarted:
    #         self.setupPolling(api_url)
    #         self.pollingStarted = True
    #     elif not api_url:
    #         QMessageBox.warning(self, 'Warning', '请先输入api')
    #
    # #设置轮询接收任务信息
    # def setupPolling(self, api_url):
    #     self.pollingTimer = QTimer(self)
    #     self.pollingTimer.timeout.connect(lambda: self.fetchData(api_url))
    #     self.pollingTimer.start(4000)  # 每 5 秒执行一次 fetchData
    #
    # def fetchData(self, api_url):
    #     # 使用传入的 api_url 发起请求
    #     self.taskFetcherThread = TaskFetcherThread(api_url)
    #     self.taskFetcherThread.finished.connect(self.processTaskData)
    #     self.taskFetcherThread.start()
    #
    #
    # def onStartDetectClicked(self):
    #     # if self.currentTaskNumber is not None:
    #     #     self.captured_images.clear()  # 清空存储的图像列表
    #     #     self.showTaskDialog(self.currentTaskNumber)
    #     # else:
    #     #     QMessageBox.warning(self, 'Warning', 'Please select a task first.')
    #     #todo test
    #     self.captured_images.clear()  # 清空存储的图像列表
    #     self.showTaskDialog(self.currentTaskNumber)
    #
    # def processTaskData(self, tasks=None):
    #     if tasks is None:
    #         # 模拟数据
    #         tasks = [
    #             {
    #                 "批号": "CY32403",
    #                 "物料类型": "小盒",
    #                 "产品物料名称": "复方酮康唑发用洗剂15+0.25毫克50毫升成品（Rx）",
    #                 "生产日期": "2023/11/24",
    #                 "有效期至": "2025/11/23",
    #                 "产线": "支装三线",
    #                 "任务序号": 1,
    #                 "检测数量": 8}
    #             #{
    #             #     "批号": "CY32403",
    #             #     "物料类型": "小盒",
    #             #     "产品物料名称": "复方酮康唑发用洗剂15+0.25毫克50毫升成品（Rx）",
    #             #     "生产日期": "2023/11/24",
    #             #     "有效期至": "2025/11/23",
    #             #     "产线": "支装三线",
    #             #     "任务序号": 2,
    #             #     "检测数量": 7
    #             # },{
    #             #     "批号": "CY32403",
    #             #     "物料类型": "小盒",
    #             #     "产品物料名称": "复方酮康唑发用洗剂15+0.25毫克50毫升成品（Rx）",
    #             #     "生产日期": "2023/11/24",
    #             #     "有效期至": "2025/11/23",
    #             #     "产线": "支装三线",
    #             #     "任务序号": 3,
    #             #     "检测数量": 5
    #             #}
    #             # # 可以添加更多模拟任务
    #         ]
    #     self.taskModel.clear()
    #     for task in tasks:
    #         task_info = "批号：{}\n物料类型：{}\n产品物料名称：{}\n生产日期：{}\n有效期至：{}\n产线：{}\n任务序号：{}\n检测数量：{}".format(
    #             task["批号"], task["物料类型"], task["产品物料名称"], task["生产日期"],
    #             task["有效期至"], task["产线"], task["任务序号"], task["检测数量"]
    #         )
    #         item = QStandardItem(task_info)
    #         self.taskModel.appendRow(item)
    #
    # def onTaskClicked(self, index: QModelIndex):
    #     task_info = index.data()  # 获取选中项的数据
    #     self.currentTaskNumber = self.parseTaskNumber(task_info)  # 存储任务序号
    #     # 假设任务序号在 task_info 字符串中，需要解析出来
    #     self.task_number = self.parseTaskNumber(task_info)
    #     #用于更改pushButton的颜色状态
    #     detection_count = self.parseDetectionCount(task_info)
    #     self.updateButtonColors(detection_count)
    #
    # def parseDetectionCount(self, task_info):
    #     # 假设任务信息格式为 "检测数量：x"，并且在字符串的末尾
    #     try:
    #         return int(task_info.split('检测数量：')[-1])
    #     except (ValueError, IndexError):
    #         return 0
    # ##用于更改pushButton的颜色状态
    # def updateButtonColors(self, detection_count):
    #     # 将所有按钮重置为默认颜色
    #     for i in range(1, 9):
    #         getattr(self, f'pushButton_{i}').setStyleSheet('')
    #
    #     # 根据检测数量设置颜色
    #     for i in range(1, detection_count + 1):
    #         getattr(self, f'pushButton_{i}').setStyleSheet('background-color: gray;')
    #
    #     # 检查 label 是否显示图片，若显示则设置为绿色
    #     for i in range(1, 9):
    #         label = getattr(self, f'label_{i}')
    #         if label.pixmap() and not label.pixmap().isNull():
    #             getattr(self, f'pushButton_{i}').setStyleSheet('background-color: green;')
    #
    # def parseTaskNumber(self, task_info):
    #     # 解析任务序号，这取决于您的任务信息格式
    #     # 以下为示例，可能需要根据实际格式调整
    #     return task_info.split('\n')[6].split('：')[1]
    # def showTaskDialog(self, task_number):
    #     task_name = f"是否确定执行任务{task_number}"
    #     dialog = TaskDialog(task_name)
    #     result = dialog.exec_()
    #     if result:
    #         print("开始检测任务")
    #         # 可以选择在这里关闭相机，或者保持打开状态
    #         if self.camera_worker.isRunning():
    #             self.camera_worker.stop()
    #             self.camera_worker.wait()
    #         self.detectTask()  # 调用检测任务函数
    #     else:
    #         print("任务取消")
    #
    # def detectTask(self):
    #     self.thread = OcrThread(self.captured_images)  # 使用捕获的图像
    #     self.thread.finished.connect(self.onOcrFinished)
    #     self.thread.start()
    #
    # def onOcrFinished(self, results):
    #     # 处理OCR结果
    #     for label_index, result in results:
    #         print(f"在 label_{label_index + 1} 的检测结果：", result)
    #     # 可以在这里更新UI等
    # def display_image_on_label(self, image_np):
    #     # 同时将图像存储在列表中
    #     self.captured_images.append(image_np)
    #     # 显示图像在当前标签上
    #     q_image = QImage(image_np.data, image_np.shape[1], image_np.shape[0], QImage.Format_RGB888)
    #     pixmap = QPixmap.fromImage(q_image)
    #     self.labels[self.current_label_index].setPixmap(
    #         pixmap.scaled(self.labels[self.current_label_index].size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
    #
    # def closeEvent(self, event):
    #     # 确保相机线程被正确关闭
    #     if self.camera_worker.isRunning():
    #         self.camera_worker.stop()
    #         self.camera_worker.wait()
    #     event.accept()
    #
    # def onTakePictureClicked(self):
    #     if not self.isCameraStarted:
    #         self.clearLabels()
    #         self.start_camera_view()
    #         self.takePictureButton.setText("关闭")
    #         self.isCameraStarted = True
    #     else:
    #         if self.camera_worker.isRunning():
    #             self.camera_worker.stop()
    #             self.camera_worker.wait()
    #         self.takePictureButton.setText("启动")
    #         self.isCameraStarted = False
    #
    # def clearLabels(self):
    #     for label in self.labels:
    #         label.clear()  # 清空标签上的图片
    # def start_camera_view(self):
    #     # 检查相机是否已经初始化
    #     if not hasattr(self, 'camera'):
    #         # 初始化相机
    #         self.init_camera()
    #         # 启动相机工作线程
    #         self.camera_worker.start()
    #
    #     # 更新 UI 状态
    #     if self.current_label_index < len(self.labels):
    #         # 切换到当前标签对应的页面
    #         self.stackedWidget.setCurrentIndex(self.current_label_index)
    #
    #
    # def capture_image(self):
    #     # 从相机捕获图像，并显示在当前标签上
    #     state = mphdc.GetCamearState(self.camera)
    #     if state == mphdc.DeviceStateType.StandBy:
    #         res, data = mphdc.SanpCamera(self.camera, 2000)
    #         if res:
    #             imgs, n, _ = mphdc.Nppc_Create(data)
    #             if n > 0:
    #                 self.display_image_on_label(imgs[0])
    #             else:
    #                 print("未捕获到图像")
    #         else:
    #             print("拍摄失败")
    # def take_photo_and_skip(self):
    #     #todo
    #     # 捕获当前图像
    #     self.capture_image()
    #     # 移动到下一个标签
    #     self.current_label_index += 1
    #     # 检查是否已到达标签列表的末尾
    #     if self.current_label_index < len(self.labels):
    #         # 更新当前显示的标签和页面
    #         self.stackedWidget.setCurrentIndex(self.current_label_index)
    #         # 如果不是最后一个标签，重启相机预览线程
    #         self.camera_worker.start()
    #     else:
    #         # 如果是最后一个标签，则重置索引
    #         self.current_label_index = 0
    #         # 可以选择在这里关闭相机，或者保持打开状态
    #         if self.camera_worker.isRunning():
    #             self.camera_worker.stop()
    #             self.camera_worker.wait()
    #
    # def take_photos1(self):
    #     filenames, _ = QFileDialog.getOpenFileNames(self, "Select Images", "", "Image Files (*.png *.jpg *.jpeg *.bmp)")
    #     if not filenames:
    #         return
    #
    #     for i, filename in enumerate(filenames[:8]):
    #         pixmap = QPixmap(filename)
    #         self.labels[i].setPixmap(pixmap.scaled(self.labels[i].size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
    #         self.labels[i].setScaledContents(True)
    #         # 如果 label 显示了图片，将对应的 pushButton 颜色设置为绿色
    #         if not pixmap.isNull():
    #             getattr(self, f'pushButton_{i + 1}').setStyleSheet('background-color: green;')
    #
    # def get_workstation_number(self, username):
    #     # 用您的数据库连接信息替换以下内容
    #     connection = dbConnect()
    #
    #     try:
    #         with connection.cursor() as cursor:
    #             sql = "SELECT number FROM dbo.users WHERE username = ?"
    #             cursor.execute(sql, (username,))
    #             result = cursor.fetchone()
    #             return result['number'] if result else None
    #     finally:
    #         connection.close()


#创建应用实例和窗口，然后运行
# app = QApplication(sys.argv)
# window = PicturePage()
# window.showMaximized()
# sys.exit(app.exec_())
