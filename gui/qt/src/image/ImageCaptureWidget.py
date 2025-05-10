from PIL.ImageQt import QPixmap
from PyQt6.QtCore import QTimer, pyqtSlot, Qt, pyqtSignal
from PyQt6.QtGui import QImage, QKeyEvent
from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QFrame, QHBoxLayout

from gui.qt.src.common.CommonObject import CommonObject
from gui.qt.src.worker.ImageCaptureWorker import ImageCaptureWorker
from src.main.client import Client
import os


class ImageCaptureWidget(QWidget):
    go_next = pyqtSignal()

    def __init__(self, parent:CommonObject=None):
        super().__init__()
        self.parent = parent
        self.data_manager = parent.data_manager
        self.image_count = 0
        self.initUI()

    def initUI(self):
        self.state_lb = QLabel("대기 중", self)
        self.count_lb = QLabel("0/6", self)
        self.photo_img_lb = QLabel(self)
        pixmap = QPixmap("gui/qt/img/take_photo_start.png")
        pixmap = pixmap.scaled(300,600, Qt.AspectRatioMode.KeepAspectRatio)
        self.photo_img_lb.setPixmap(pixmap)
        self.count_lb.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.state_lb.setStyleSheet("""background-color: rgb(255, 255, 255); color: rgb(0, 0, 0); font-size: 20px;""")
        self.state_lb.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.count_lb.setStyleSheet("font-size: 20px;")
        self.image_lb = QLabel(self)
        self.image_lb.setAlignment(Qt.AlignmentFlag.AlignCenter)

        vbox = QVBoxLayout()
        vbox.addWidget(self.state_lb,1)
        vbox.addWidget(self.count_lb,1)
        vbox.addWidget(self.photo_img_lb,7)

        hbox = QHBoxLayout()
        hbox.addLayout(vbox)
        hbox.addWidget(self.image_lb,9)

        self.setLayout(hbox)
        self.setUI()

    def setUI(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.countDown)

        self.image_worker = ImageCaptureWorker(self)
        self.image_worker.imageCaptured.connect(self.setImage)
        self.client = Client()
        self.image_worker.start()

    def startCapture(self):
        self.image_worker.go = True
        self.data_manager.makePhotoDirectory()
        # self.image_worker.start()

    def endCapture(self):
        self.state_lb.setText("대기 중")
        self.count_lb.setText("0/6")
        self.image_lb.clear()
        self.image_count = 0
        # self.image_worker.stop()

    def countDownStart(self):
        self.count = 5
        self.timer.start(1000)
        self.countDown()

    def saveImage(self):
        image_path = os.path.join(self.data_manager.photo_save_dir_path, str(self.image_count) + ".png")
        self.image_worker.saveImage(image_path)

    def countDown(self):
        if self.count == 0:
            self.state_lb.setText("찰칵")
            self.image_count +=1
            self.count_lb.setText(f"{self.image_count}/6")
            self.count = 5
            self.saveImage()
            if self.image_count == 6:
                self.timer.stop()
                self.go_next.emit()
            return
        self.state_lb.setText(f"{self.count}초")
        self.count -= 1

    @pyqtSlot(QImage)
    def setImage(self, image:QImage):
        resized_image = QImage.scaled(image, self.image_lb.width(), self.image_lb.height(), Qt.AspectRatioMode.KeepAspectRatio)
        self.current_image = image
        pixmap:QPixmap = QPixmap.fromImage(resized_image)
        self.image_lb.setPixmap(pixmap)

    def onKeyPressEvent(self, event:QKeyEvent):
        key = event.key()
        match key:
            case Qt.Key.Key_T:
                self.countDownStart()


