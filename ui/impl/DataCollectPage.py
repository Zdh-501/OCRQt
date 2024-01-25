import os
import subprocess
import sys
import json  # 导入json模块

from PyQt5.QtCore import Qt
from PyQt5.QtCore import QThread
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication
from pyqt5_plugins.examplebutton import QtWidgets

from mphdcpy import mphdc
from ui.layout.UI_DataCollectPage import Ui_DataCollectPage
from ui.impl.myThread import *
class WorkerThread(QThread):
    def __init__(self, command, working_dir):
        super().__init__()
        self.command = command
        self.working_dir = working_dir

    def run(self):
        subprocess.run(self.command, cwd=self.working_dir)

class DataCollectPage(QtWidgets.QWidget,Ui_DataCollectPage):
    def __init__(self):
        super(DataCollectPage, self).__init__()
        self.setupUi(self)  # 从UI_DataCollectPage.py中加载UI定义
        self.is_camera_initialized = False

        #todo 读取配置文件 此处要改成绝对路径
        with open('D:\\config.json', 'r') as config_file:
            self.config = json.load(config_file)

        self.labelButton.clicked.connect(self.startPPOCRLabel)
        self.startButton.clicked.connect(self.start_camera_view)


        self.kdBox.setChecked(False)  # 初始状态未选中
        self.kdBox.stateChanged.connect(self.updateBoxes)

        self.normMixBox.setChecked(True)  # 初始状态选中
        self.normMixBox.stateChanged.connect(self.updateBoxes)


    def updateBoxes(self):
        # 当一个勾选框被选中时，另一个自动取消选中
        sender = self.sender()
        if sender == self.kdBox and self.kdBox.isChecked():
            self.normMixBox.setChecked(False)

            # 通知CameraWorker线程更新active_channels
            self.camera_worker.active_channels = ['kd']
        elif sender == self.normMixBox and self.normMixBox.isChecked():
            self.kdBox.setChecked(False)

            # 通知CameraWorker线程更新active_channels
            self.camera_worker.active_channels = ['nx', 'ny', 'nz']
        elif not self.kdBox.isChecked() and not self.normMixBox.isChecked():
            # 如果两个都没有被选中，则自动选中normMixBox
            self.normMixBox.setChecked(True)

    def start_camera_view(self):

        # 检查相机是否已经初始化
        if not hasattr(self, 'camera'):
            # 初始化相机
            self.init_camera()
            self.is_camera_initialized = True
            self.startButton.setText('暂停')  # 假设相机初始化后即开始捕获
        elif self.is_camera_initialized:
            if not self.camera_worker._is_paused:
                # 如果相机正在运行，则暂停相机，并将按钮文本设置为"开始"
                self.camera_worker.pause()  # 假设camera_worker有一个pause方法
                self.startButton.setText('启动相机')
            else:
                # 如果相机已经暂停，则恢复相机，并将按钮文本设置为"暂停"
                self.camera_worker.resume()  # 假设camera_worker有一个resume方法
                self.startButton.setText('暂停')
    def init_camera(self):
        self.camera = mphdc.CreateCamera(ct.c_int(mphdc.LogMediaType.Off.value), ct.c_int(1))

        mphdc.UpdateCameraList(self.camera)

        camera_info = mphdc.GetCameraInfo(self.camera, 0)
        mphdc.OpenCamera(self.camera, camera_info)
        if mphdc.GetCameraState(self.camera):
            mphdc.SetHoldState(self.camera,False)

        # 设置相机触发模式
        mphdc.SetCamera_Triggersource(self.camera)

        # 默认设置相机激活nx, ny, nz,kd通道
        mphdc.SetPhotometricOutputChannelEnable(self.camera, ['nx', 'ny', 'nz','kd'])

        # 设置相机为光度立体模式，并指定输出通道
        self.set_camera_photometric_settings()
        # 创建CameraWorker线程
        self.camera_worker = CameraWorker(self.camera)

        # 连接 image_captured 信号到 display_image_on_label 方法
        self.camera_worker.image_captured.connect(self.display_image_on_label)

        self.camera_worker.start()

    def set_camera_photometric_settings(self):
        # 设置光源为外接光源
        light_settings = mphdc.GetLightSettings(self.camera)

        light_settings.LightSourceSelection = mphdc.LightSourceSelectionType.ExternalLight.value
        mphdc.SetLightSettings(self.camera, light_settings)

        # 设置光度立体算法模式
        photometric_settings = mphdc.GetPhotometricSettings(self.camera)
        photometric_settings.AlgorithmMode = mphdc.PhotometricAlgorithmModeType.Fast.value
        #todo 添加修改通道

        mphdc.SetPhotometricSettings(self.camera, photometric_settings)
    def display_image_on_label(self, image_np):
        # 显示图像在当前标签上
        q_image = QImage(image_np.data, image_np.shape[1], image_np.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)
        pixmap = pixmap.scaled(self.label_5.width(), self.label_5.height(), Qt.KeepAspectRatio)
        self.label_5.setPixmap(pixmap)
    def startPPOCRLabel(self):
        # 直接使用配置文件中的绝对路径
        working_dir = self.config["PPOCRLabel_working_dir"]
        command = ['PPOCRLabel', '--lang', 'ch']

        self.workerThread = WorkerThread(command, working_dir)
        self.workerThread.start()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = DataCollectPage()
    mainWindow.show()
    app.exec_()