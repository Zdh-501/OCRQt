import requests
from PyQt5.QtCore import QThread, pyqtSignal, QBuffer, QIODevice
import numpy as np
from mphdcpy import mphdc
from PIL import Image
from io import BytesIO
from paddleocr import PaddleOCR
import ctypes as ct
import time
class TaskFetcherThread(QThread):
    finished = pyqtSignal(list)  # 发射任务列表

    def __init__(self, api_url):
        super().__init__()
        self.api_url = api_url

    def run(self):
        try:
            response = requests.get(self.api_url)
            response.raise_for_status()
            tasks = response.json()  # 假设 API 返回 JSON 数据
            self.finished.emit(tasks)
        except requests.RequestException as e:
            self.finished.emit([])  # 发射空列表或处理错误
# 定义图像捕获线程类
class CameraWorker(QThread):
    image_captured = pyqtSignal(np.ndarray)

    def __init__(self, camera):
        super().__init__()
        self.camera = camera
        self._is_running = True

    def run(self):
        while self._is_running:
            state = mphdc.GetCamearState(self.camera)
            if state == mphdc.DeviceStateType.StandBy:
                res, data = mphdc.SanpCamera(self.camera, 2000)
                if res:
                    imgs, n, _ = mphdc.Nppc_Create(data)
                    if n > 0:
                        self.image_captured.emit(imgs[0])

    def stop(self):
        self._is_running = False

# OCR检测子线程
class OcrThread(QThread):
    finished = pyqtSignal(object)  # 完成信号，传递检测结果

    def __init__(self, images, parent=None):
        super().__init__(parent)
        self.images = images  # NumPy图像数组列表
        self.ocr = PaddleOCR(use_angle_cls=True, lang='en')  # 根据需要调整参数

    def run(self):
        results = []
        for i, image_np in enumerate(self.images):
            result = self.ocr.ocr(image_np, cls=True)
            results.append((i, result))
        self.finished.emit(results)  # 发送完成信号，附带检测结果