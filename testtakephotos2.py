import ctypes as ct
import numpy as np
from mphdcpy import mphdc
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QStackedWidget, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap

from ui.impl.myThread import *

class PicturePage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.init_camera()
        self.current_label_index = 0

    def init_ui(self):
        self.labels = [QLabel(f'label_{i}') for i in range(1, 9)]
        self.takePictureButton = QPushButton('开始')
        self.takePictureButton.clicked.connect(self.start_camera_view)
        self.skipButton = QPushButton('跳过')
        self.skipButton.clicked.connect(self.take_photo_and_skip)
        self.stackedWidget = QStackedWidget()
        for label in self.labels:
            self.stackedWidget.addWidget(label)
        layout = QVBoxLayout()
        layout.addWidget(self.takePictureButton)
        layout.addWidget(self.skipButton)
        layout.addWidget(self.stackedWidget)
        self.setLayout(layout)

    def init_camera(self):
        self.camera = mphdc.CreateCamera(ct.c_int(mphdc.LogMediaType.Off.value), ct.c_int(1))
        mphdc.UpdateCameraList(self.camera)
        camera_info = mphdc.GetCameraInfo(self.camera, 0)
        mphdc.OpenCamera(self.camera, camera_info)
        self.camera_thread = CameraThread(self.camera)
        self.camera_thread.image_captured.connect(self.display_image_on_label)
        self.camera_thread.start()

    def display_image_on_label(self, image_np):
        current_label = self.labels[self.current_label_index]
        q_image = QImage(image_np.data, image_np.shape[1], image_np.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)
        current_label.setPixmap(pixmap.scaled(current_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def start_camera_view(self):
        self.stackedWidget.setCurrentIndex(self.current_label_index)

    def take_photo_and_skip(self):
        self.current_label_index += 1
        if self.current_label_index >= len(self.labels):
            self.current_label_index = 0  # Reset index if it exceeds the limit
        self.stackedWidget.setCurrentIndex(self.current_label_index)

    def closeEvent(self, event):
        if self.camera_thread.isRunning():
            self.camera_thread.stop()
        mphdc.CloseCamera(self.camera)
        mphdc.DeleteCamera(self.camera)
        super().closeEvent(event)

# 主程序部分
app = QApplication([])
window = PicturePage()
window.show()
app.exec_()
