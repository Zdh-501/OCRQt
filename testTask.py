import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QProgressBar, QStackedWidget, QLabel, QVBoxLayout, QWidget

class PhotoTaskApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.layout = QVBoxLayout(self.centralWidget)

        self.progressBar = QProgressBar(self)
        self.stackedWidget = QStackedWidget(self)

        self.layout.addWidget(self.stackedWidget)
        self.layout.addWidget(self.progressBar)

        # 示例：创建一个具有10个任务的任务
        self.createTask(10)

    def createTask(self, photo_count):
        self.progressBar.setMaximum(photo_count)

        for i in range(photo_count):
            label = QLabel(f"Photo {i + 1}", self)

            self.stackedWidget.addWidget(label)

        self.progressBar.valueChanged.connect(self.stackedWidget.setCurrentIndex)

    # 在这里添加切换任务的逻辑
    # ...

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PhotoTaskApp()
    ex.show()
    sys.exit(app.exec_())
