import os
import subprocess
import sys
import json  # 导入json模块

from PyQt5.QtCore import Qt
from PyQt5.QtCore import QThread
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMessageBox
from pyqt5_plugins.examplebutton import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from mphdcpy import mphdc
from ui.layout.UI_DataCollectPage import Ui_DataCollectPage
from ui.impl.myThread import *

class DataCollectPage(QtWidgets.QWidget,Ui_DataCollectPage):
    def __init__(self):
        super(DataCollectPage, self).__init__()
        self.setupUi(self)  # 从UI_DataCollectPage.py中加载UI定义
        self.is_camera_initialized = False

        #todo 读取配置文件 此处要改成绝对路径
        with open('D:\\config.json', 'r') as config_file:
            self.config = json.load(config_file)

        self.kdBox.setChecked(False)  # 初始状态未选中
        self.kdBox.stateChanged.connect(self.updateBoxes)

        self.normMixBox.setChecked(True)  # 初始状态选中
        self.normMixBox.stateChanged.connect(self.updateBoxes)

        self.exposureSlider.setMinimum(1)
        self.exposureSlider.setMaximum(100)
        self.exposureSlider.setValue(50)  # 初始值设为50

        self.labelButton.clicked.connect(self.startPPOCRLabel)
        self.startButton.clicked.connect(self.start_camera_view)
        self.takepictureButton.clicked.connect(self.save_picture)
        self.saveButton.clicked.connect(self.choose_save_path)
        self.zeroButton.clicked.connect(self.reset_count)

        # 连接sliderReleased信号到changeExposure槽函数
        self.exposureSlider.sliderReleased.connect(self.changeExposure)

    def reset_count(self):
        # 弹出确认提示框
        reply = QMessageBox.question(self, '重置计数', '是否要重新计数？', QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            # 如果用户选择“是”，则将countLabel的数值重置为0
            self.countLabel.setText("0")
    def choose_save_path(self):
        # 弹出文件夹选择对话框
        directory = QFileDialog.getExistingDirectory(self, "选择保存路径", "")

        # 如果用户选择了路径，则更新saveEdit的内容
        if directory:
            self.saveEdit.setText(directory)
    def save_picture(self):
        # 确保相机已初始化并且正在运行
        if not (hasattr(self, 'is_camera_initialized') and self.is_camera_initialized and
                hasattr(self, 'camera_worker') and not self.camera_worker.is_paused()):
            QMessageBox.warning(self, "相机未运行", "请先启动并运行相机")
            return
        # 获取保存的格式
        file_format = self.formatBox.currentText()
        if not file_format:
            QMessageBox.warning(self, "错误", "请选择图片的格式")
            return

        # 获取输入的文件名
        base_filename = self.nameEdit.text().strip()  # .strip() 删除可能的前后空格
        if not base_filename:
            QMessageBox.warning(self, "错误", "请输入文件的基础名称")
            return
        # 获取计数器内容
        count = self.countLabel.text()
        # 生成最终的文件名
        filename = f"{base_filename}_{count}.{file_format}"
        filename = filename.encode('utf-8').decode(sys.getfilesystemencoding())
        # 获取保存路径
        save_path = self.saveEdit.text()
        if not save_path:
            QMessageBox.warning(self, "错误", "请选择或输入保存路径")
            return
        full_path = os.path.join(save_path, filename)
        full_path = full_path.encode('utf-8').decode('utf-8')
        #todo 中文乱码还未解决
        # 检查图像是否可用（这里假设您已经有了当前图像的np.ndarray）
        if hasattr(self, 'current_image') and self.current_image is not None:
            # 创建并启动图像保存线程
            self.image_save_thread = ImageSaveThread(self.current_image, full_path, file_format)
            self.image_save_thread.save_finished.connect(self.on_save_finished)  # 连接信号
            self.image_save_thread.start()
        else:
            QMessageBox.warning(self, "错误", "当前没有可用的图像")

    def on_save_finished(self, message):
        if "图像已保存" in message:
            # 获取当前计数值并增加1
            current_count = int(self.countLabel.text())
            self.countLabel.setText(str(current_count + 1))

        QMessageBox.information(self, "信息", message)

    def updateBoxes(self):
        # 当一个勾选框被选中时，另一个自动取消选中
        sender = self.sender()
        if sender == self.kdBox and self.kdBox.isChecked():
            self.normMixBox.setChecked(False)
            if self.is_camera_initialized:
                # 通知CameraWorker线程更新active_channels
                self.camera_worker.active_channels = ['kd']
        elif sender == self.normMixBox and self.normMixBox.isChecked():
            self.kdBox.setChecked(False)
            if self.is_camera_initialized:
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

        # 更新当前图像 用于拍照保存
        self.current_image = image_np

    def changeExposure(self):
        value = self.exposureSlider.value()
        # 检查self.camera是否已经初始化
        if self.is_camera_initialized:  # 假设有一个标志或方法可以检查相机是否初始化
            exposure_value = value  # 根据滑动条的值设置曝光值
            # 检查曝光值是否在0-100之间
            if 0 <= exposure_value <= 100:
                res = mphdc.SetPhotometricExposureIntensityMain(self.camera, exposure_value)
                if not res:
                    QMessageBox.warning(self, "错误", "设置光度立体主计算图曝光强度失败！")
                # 更新曝光值显示标签
                self.exposureValueLabel.setText(f"{value}")
            else:
                QMessageBox.warning(self, "曝光值错误", "曝光强度必须在0到100之间。")
        else:
            self.exposureSlider.setValue(50)  # 初始值设为50
            QMessageBox.warning(self, "相机未初始化", "请先启动相机，再调整曝光值")


    def startPPOCRLabel(self):

        # 设置 PPOCRLabel 的工作目录为 PaddleOCR 文件夹
        working_dir = "PaddleOCR" #ModeMainPage启动点和PaddleOCR目录同级
        # PPOCRLabel 的命令，假设 PPOCRLabel 是一个可执行的文件或者正确配置了环境变量
        command = ['PPOCRLabel', '--lang', 'ch']

        self.labelThread = LabelThread(command, working_dir)
        self.labelThread.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = DataCollectPage()
    mainWindow.show()
    app.exec_()