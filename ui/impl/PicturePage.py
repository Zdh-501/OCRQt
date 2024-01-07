import sys

from PyQt5 import QtCore

from PyQt5.QtGui import QPixmap, QImage, QFontMetrics
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from pyqt5_plugins.examplebutton import QtWidgets
from pyqt5_plugins.examplebuttonplugin import QtGui


from ui.layout.UI_PicturePage import Ui_PicturePage
from ui.impl.TaskDialog import TaskDialog
from ui.impl.myThread import *


class PicturePage(QtWidgets.QWidget, Ui_PicturePage):
    def __init__(self):
        super(PicturePage, self).__init__()
        self.setupUi(self)
        self.count = 0  # 初始化 count 属性
        self.detection_type="单面"  #初始化 detection_type 属性
        # 初始化 PaddleOCR 配置
        self.det_model_dir = r"D:/Paddle/ResNet50_1220"
        self.rec_model_dir = "D:/Paddle/rec"
        self.use_angle_cls = True
        self.det_db_unclip_ratio = 2.8
        self.lang = 'en'
        #用于区分手动捕获照片还是子线程自动捕获
        self.should_store_captured_image = False
        # 创建 PaddleOCR 实例
        self.initialize_ocr()

        self.current_label_index = 0
        self.currentTaskNumber = None  # 添加一个变量来存储当前选中的任务序号
        self.isCameraStarted = False  # 相机是否已启动的标志
        self.captured_images = []  # 用于存储捕获的图像
        self.task_completion_status = []  # 初始化任务完成状态列表

        
        self.startDetectButton.clicked.connect(self.onStartDetectClicked)
        self.takePictureButton.clicked.connect(self.start_camera_view)
        self.skipButton.clicked.connect(self.take_photo_and_skip)

        current_username = 'root'
        workstation_number = self.get_workstation_number(current_username)
        if workstation_number is not None:
            self.textBrowser_2.setText(f"生产工位: {workstation_number}")
        else:
            self.textBrowser_2.setText("生产工位：")
    def init_camera(self):
        self.camera = mphdc.CreateCamera(ct.c_int(mphdc.LogMediaType.Off.value), ct.c_int(1))
        mphdc.UpdateCameraList(self.camera)

        camera_info = mphdc.GetCameraInfo(self.camera, 0)
        mphdc.OpenCamera(self.camera, camera_info)


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

        # 清除旧数据
        self.tableWidget_2.clearContents()
        self.tableWidget_2.setRowCount(len(item_details))

        # 设置表格列数和表头
        self.tableWidget_2.setColumnCount(2)
        self.tableWidget_2.setHorizontalHeaderLabels(["属性", "值"])

        # 填充数据
        for row, (key, value) in enumerate(item_details.items()):
            self.tableWidget_2.setItem(row, 0,  QtWidgets.QTableWidgetItem(key))
            self.tableWidget_2.setItem(row, 1, QtWidgets.QTableWidgetItem(value))

        # 调整列宽以自适应内容
        self.tableWidget_2.resizeColumnsToContents()

        # 获取当前字体
        font = self.tableWidget_2.font()

        # 使用 QFontMetrics 获取字体相关的尺寸信息
        font_metrics = QFontMetrics(font)
        text_height = font_metrics.height()

        # 为了留出一些额外空间，可以在文本高度的基础上增加一些像素
        padding = 4  # 可以根据需要调整这个值
        row_height = text_height + padding

        # 设置每行的高度
        for row in range(self.tableWidget_2.rowCount()):
            self.tableWidget_2.setRowHeight(row, row_height)

        # 使第一列根据内容自动调整宽度
        self.tableWidget_2.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        # 使第二列填满剩余宽度
        self.tableWidget_2.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

    def setLabelsAndPages(self, count, detection_type):
        self.count = count  # 更新类属性
        self.task_completion_status = [False] * count  # False 表示任务未完成
        # 根据检测类型显示或隐藏第二个进度条
        if detection_type == "单面":
            self.progressBar_2.hide()
            self.progressBar.setShouldDrawText(False)  # 不绘制文本

        elif detection_type == "双面":
            self.detection_type="双面"
            self.progressBar.setShouldDrawText(True)  # 不绘制文本
            self.progressBar_2.show()

        self.progressBar.setSegmentCount(count)
        self.progressBar_2.setSegmentCount(count)
        # 清除当前的所有 pages 和 labels
        while self.stackedWidget.count() > 0:
            widget_to_remove = self.stackedWidget.widget(0)
            self.stackedWidget.removeWidget(widget_to_remove)
            widget_to_remove.deleteLater()
        self.labels_1 = []
        self.labels_2 = []
        self.pages_1 = []
        self.pages_2 = []
        for i in range(count):
            # 创建 label
            label = QtWidgets.QLabel(f"产品 {i + 1}")
            label.setAlignment(QtCore.Qt.AlignCenter)  # 设置 label 文字居中显示
            # 创建并设置字体
            font = QtGui.QFont()
            font.setPointSize(16)  # 设置字体大小为12点
            label.setFont(font)
            self.labels_1.append(label)
            # 创建 page
            page = QtWidgets.QWidget()
            layout = QtWidgets.QVBoxLayout()  # 创建 QVBoxLayout
            layout.addWidget(label)  # 将 label 添加到 QVBoxLayout
            page.setLayout(layout)  # 设置 page 的布局
            self.pages_1.append(page)
            # 将 page 添加到 QStackedWidget
            self.stackedWidget.addWidget(page)

        for i in range(count):
            # 创建 label
            label = QtWidgets.QLabel(f"产品{i + 1}")
            label.setAlignment(QtCore.Qt.AlignCenter)  # 设置 label 文字居中显示
            # 创建并设置字体
            font = QtGui.QFont()
            font.setPointSize(16)  # 设置字体大小为12点
            label.setFont(font)
            self.labels_2.append(label)
            # 创建 page
            page = QtWidgets.QWidget()
            layout = QtWidgets.QVBoxLayout()  # 创建 QVBoxLayout
            layout.addWidget(label)  # 将 label 添加到 QVBoxLayout
            page.setLayout(layout)  # 设置 page 的布局
            self.pages_2.append(page)
            # 将 page 添加到 QStackedWidget
            self.stackedWidget.addWidget(page)

        # 如果需要，可以在此处设置 QStackedWidget 显示第一页
        self.stackedWidget.setCurrentIndex(0)
        #进度条等分
        self.progressBar.setMaximum(count)
        self.progressBar.setMinimum(0)
        self.progressBar.clickedValue.connect(self.onProgressBarClicked)

        self.progressBar_2.setMaximum(count)
        self.progressBar_2.setMinimum(0)
        self.progressBar_2.clickedValue.connect(self.onProgressBarClicked)

    def isPhotoDisplayedOnLabel(self, label):
        # 检查label是否显示了照片，这需要根据您的应用程序具体实现
        # 例如，您可能会检查label的pixmap是否非空
        return label.pixmap() is not None and not label.pixmap().isNull()
    def onProgressBarClicked(self, value):
        sender = self.sender()
        whichPart = value

        # 计算前一个任务的索引
        prev_task_index = whichPart - 1

        # 检查前一个任务是否已完成
        if prev_task_index >= 0 and not self.task_completion_status[prev_task_index]:
            QtWidgets.QMessageBox.warning(self, "提示", f"请先完成产品{whichPart}的检测上传任务")
            return

        if self.detection_type == "双面":
            if sender == self.progressBar:
                # 第一个进度条被点击
                self.stackedWidget.setCurrentIndex(whichPart)
            elif sender == self.progressBar_2:
                # 第二个进度条被点击
                if not self.isPhotoDisplayedOnLabel(self.labels_1[whichPart]):
                    QtWidgets.QMessageBox.warning(self, "提示", f"请先完成产品{whichPart + 1}的批号面拍摄")
                    return
                self.stackedWidget.setCurrentIndex(self.count + whichPart)

        elif self.detection_type == "单面":
            if sender == self.progressBar:
                # 第一个进度条被点击
                self.stackedWidget.setCurrentIndex(whichPart)

        # 更新进度条的值（如果您希望点击进度条后进度条也反映当前页面）
        if sender == self.progressBar:
            self.progressBar.setValue(whichPart + 1)
        elif sender == self.progressBar_2:
            self.progressBar_2.setValue(whichPart + 1)



    def onStartDetectClicked(self):

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
        self.captured_images.clear()  # 清空存储的图像列表
        # 当前任务的索引
        task_index = self.current_label_index // 2 if self.detection_type == "双面" else self.current_label_index
        # 标记当前任务为完成
        if task_index <= len(self.task_completion_status):
            self.task_completion_status[task_index-1] = True

        # 处理“双面”和“单面”情况下的页面切换
        if self.detection_type == "双面":
            if self.current_label_index % 2 != 0:
                # 如果刚捕获完日期面，切换到下一个产品的批号面
                next_index = (self.current_label_index + 1) // 2
                self.stackedWidget.setCurrentIndex(next_index)
        else:
            # 单面情况，直接显示下一个产品
            self.stackedWidget.setCurrentIndex(self.current_label_index)

        # 更新进度条的值
        if self.detection_type == "双面":
            if self.current_label_index % 2 == 0:
                self.progressBar.setValue(self.current_label_index // 2 + 1)
            else:
                self.progressBar_2.setValue(self.current_label_index // 2 + 1)
        else:
            self.progressBar.setValue(self.current_label_index + 1)

        # 处理OCR结果
        for label_index, result in results:
            print(f"在 label_{label_index + 1} 的检测结果：", result)
        # 可以在这里更新UI等

    def display_image_on_label(self, image_np):
        # todo 同时将图像存储在列表中,要补充存在本地中
        if self.should_store_captured_image:
            # 只有在标志为True时，才将图像添加到列表中
            self.captured_images.append(image_np)
            # 重置标志，以便下一次点击时再次检查
            self.should_store_captured_image = False

        # 显示图像在当前标签上
        q_image = QImage(image_np.data, image_np.shape[1], image_np.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)

        # 根据检测类型选择使用 self.labels_1 或 self.labels_2
        if self.current_label_index<self.count*2 :
            if  self.detection_type == "双面":
                # 如果是偶数次拍摄，显示在self.labels_1，否则显示在self.labels_2
                target_label = self.labels_1[self.current_label_index // 2] if self.current_label_index % 2 == 0 else\
                self.labels_2[self.current_label_index // 2]
            else:
                # "单面"情况下只使用self.labels_1
                target_label = self.labels_1[self.current_label_index]
            target_label.setPixmap(pixmap.scaled(target_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

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
        # 更新进度条
        if self.current_label_index<=1:
            self.progressBar.setValue(1)


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
        # 当前任务的索引
        task_index = self.current_label_index // 2 if self.detection_type == "双面" else self.current_label_index
        # 计算上一个任务的索引
        prev_task_index = (self.current_label_index // 2 - 1) if self.detection_type == "双面" else (
                    self.current_label_index - 1)
        print(prev_task_index)
        print(task_index)
        print(self.task_completion_status)
        # 检查上一个任务是否已完成
        if prev_task_index >= 0 and not self.task_completion_status[prev_task_index]:
            QtWidgets.QMessageBox.warning(self, "提示", "请先完成本产品的检测上传再继续拍照")
            return

        self.should_store_captured_image = True
        self.capture_image()

        # 只在“双面”模式下且当前为批号面图像时切换到日期面
        if self.detection_type == "双面" and self.current_label_index % 2 == 0:
            next_index = self.current_label_index // 2 + self.count
            self.stackedWidget.setCurrentIndex(next_index)
            self.progressBar_2.setValue(self.current_label_index // 2 + 1)

        # 递增 current_label_index，不论检测类型
        self.current_label_index += 1
        # 如果需要的话，重新启动相机工作线程
        if self.current_label_index < 2 * self.count if self.detection_type == "双面" else self.count:
            self.camera_worker.start()
        else:

            if self.camera_worker.isRunning():
                self.camera_worker.stop()
                self.camera_worker.wait()




    def get_workstation_number(self, username):
       #todo
        pass


#创建应用实例和窗口，然后运行
# app = QApplication(sys.argv)
# window = PicturePage()
# window.showMaximized()
# sys.exit(app.exec_())
