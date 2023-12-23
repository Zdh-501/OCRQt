from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QStackedWidget, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer, Qt, QEvent
from PyQt5.QtGui import QImage, QPixmap
from mphdcpy import mphdc
import ctypes as ct
import numpy as np

class PicturePage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.init_camera()

        self.current_label_index = 0  # 当前显示相机画面的label索引
        #self.timer = QTimer(self)
        #self.timer.timeout.connect(self.update_camera_view)

    def init_ui(self):
        self.labels = [QLabel(f'label_{i + 1}') for i in range(8)]
        self.takePictureButton = QPushButton('拍照')
        self.skipButton = QPushButton('跳过')
        self.stackedWidget = QStackedWidget()

        for label in self.labels:
            page = QWidget()
            layout = QVBoxLayout()
            layout.addWidget(label)
            page.setLayout(layout)
            self.stackedWidget.addWidget(page)

        layout = QVBoxLayout(self)
        layout.addWidget(self.takePictureButton)
        layout.addWidget(self.skipButton)
        layout.addWidget(self.stackedWidget)

        self.takePictureButton.clicked.connect(self.start_camera_view)
        self.skipButton.clicked.connect(self.take_photo_and_advance)

    def init_camera(self):
        self.camera = mphdc.CreateCamera(ct.c_int(mphdc.LogMediaType.Off.value), ct.c_int(1))
        mphdc.UpdateCameraList(self.camera)
        camera_info = mphdc.GetCameraInfo(self.camera, 0)
        mphdc.OpenCamera(self.camera, camera_info)

        @ct.CFUNCTYPE(None, ct.c_int, mphdc.MPHDC_DataFrameUndefined)
        def datacb(datatype, mphdc_data):
            imgs, n, _ = mphdc.Nppc_Create(mphdc_data)
            if n > 0:
                QApplication.instance().postEvent(self, UpdateLabelEvent(imgs[0]))

        mphdc.mphdcapi.MPHdc_SetDataCallBack(self.camera, datacb)

    def start_camera_view(self):
        if self.current_label_index < len(self.labels):
            self.stackedWidget.setCurrentIndex(self.current_label_index)
            mphdc.SoftTiggerCamera(self.camera)

    def event(self, event):
        if isinstance(event, UpdateLabelEvent):
            self.display_image_on_label(event.image_np, self.labels[self.current_label_index])
            return True
        return super(PicturePage, self).event(event)

    def display_image_on_label(self, image_np, label):
        q_image = QImage(image_np.data, image_np.shape[1], image_np.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)
        label.setPixmap(pixmap.scaled(label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def take_photo_and_advance(self):
        self.timer.stop()  # 停止实时画面更新
        res, data = mphdc.SanpCamera(self.camera, 2000)
        if res:
            imgs, n, _ = mphdc.Nppc_Create(data)
            if n > 0:
                self.display_image_on_label(imgs[0], self.labels[self.current_label_index])

        self.current_label_index += 1
        if self.current_label_index < len(self.labels):
            self.start_camera_view()
        else:
            self.current_label_index = 0  # 重置索引

    def closeEvent(self, event):
        if self.camera:
            mphdc.CloseCamera(self.camera)
            mphdc.DeleteCamera(self.camera)
        super().closeEvent(event)

class UpdateLabelEvent(QEvent):
    def __init__(self, image_np):
        super().__init__(QEvent.User)
        self.image_np = image_np

# 主程序部分
app = QApplication([])
window = PicturePage()
window.show()
app.exec_()
