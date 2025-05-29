from PIL.ImageQt import QPixmap
from PyQt6.QtCore import QTimer, pyqtSlot, Qt, pyqtSignal, QUrl
from PyQt6.QtGui import QImage, QKeyEvent
from PyQt6.QtMultimedia import QSoundEffect
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout

from gui.common import CommonWidget
from gui.common.CommonObject import CommonObject
from gui.worker.ImageCaptureWorker import ImageCaptureWorker
import os
import time

photo_shoot_sound_url = "./gui/sound/photo_shoot.wav"

class ImageCaptureWidget(CommonWidget):
    go_next = pyqtSignal()

    def __init__(self, parent:CommonObject=None):
        super().__init__()
        self.parent = parent
        self.data_manager = parent.data_manager
        self.image_count = 0
        self.initUI()

    def initUI(self):
        self.state_lb = QLabel("대기 중", self)
        self.state_lb.setGeometry(30, 30, 100, 50)
        self.count_lb = QLabel(f"0/{self.data_manager.getPhotoCount()}", self)
        self.count_lb.setGeometry(30, 130, 100, 50)
        # self.photo_img_lb = QLabel(self)
        # pixmap = QPixmap("gui/qt/img/take_photo_start.png")
        # pixmap = pixmap.scaled(1200, 900, Qt.AspectRatioMode.KeepAspectRatio)
        # self.photo_img_lb.setPixmap(pixmap)
        # self.photo_img_lb.setGeometry(200, 0, 1200, 900)
        self.count_lb.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.state_lb.setStyleSheet("""background-color: rgb(255, 255, 255); color: rgb(0, 0, 0); font-size: 20px;""")
        self.state_lb.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.count_lb.setStyleSheet("font-size: 20px;")
        self.image_lb = QLabel(self)
        self.image_lb.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.soundEffect = QSoundEffect()
        self.soundEffect.setSource(QUrl.fromLocalFile(photo_shoot_sound_url))
        self.soundEffect.setLoopCount(1)

        vbox = QVBoxLayout()
        vbox.addWidget(self.state_lb,1)
        vbox.addWidget(self.count_lb,1)
        vbox.addStretch(7)

        hbox = QHBoxLayout()
        hbox.addWidget(self.image_lb,6)

        self.setLayout(hbox)
        self.setUI()

    def setUI(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.countDown)

        self.image_worker = ImageCaptureWorker(self)
        self.image_worker.imageCaptured.connect(self.setImage)
        self.image_worker.start()

    def startCapture(self):
        self.image_worker.setFourCutData(self.data_manager.getSelectedFrame())
        if self.data_manager.getSelectedFrame().overlayOnCam():
            self.image_worker.setCurrentOverlayIndex(0)
        else:
            self.image_worker.setCurrentOverlayIndex(-1)
            self.image_worker.setCurrentFrameImageIndex(0)
        self.count_lb.setText(f"0/{self.data_manager.getPhotoCount()}")
        self.image_count = 0
        self.image_worker.go = True
        self.data_manager.makePhotoDirectory()
        # self.image_worker.start()

    def endCapture(self):
        self.state_lb.setText("대기 중")
        self.count_lb.setText(f"0/{self.data_manager.getPhotoCount()}")
        self.image_lb.clear()
        # self.image_worker.stop()

    def countDownStart(self):
        self.count = 5
        self.timer.start(1000)
        self.countDown()

    def saveImage(self):
        image_path = os.path.join(self.data_manager.photo_save_dir_path, str(self.image_count) + ".png")
        self.image_worker.saveImage(image_path)

    def countDown(self):
        photo_count = self.data_manager.getPhotoCount()
        if self.count == 0:
            self.state_lb.setText("찰칵")
            self.image_count +=1
            self.count_lb.setText(f"{self.image_count}/{photo_count}")
            self.count = 5
            self.soundEffect.play()
            self.saveImage()
            if self.image_count == photo_count:
                self.timer.stop()
                time.sleep(1)
                self.go_next.emit()
                return
            if self.data_manager.getSelectedFrame().overlayOnCam():
                self.image_worker.setCurrentOverlayIndex(self.image_count)
            else:
                self.image_worker.setCurrentFrameImageIndex(self.image_count)
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


