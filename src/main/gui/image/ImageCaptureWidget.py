from PIL.ImageQt import QPixmap
from PyQt6.QtCore import QTimer, pyqtSlot, Qt, pyqtSignal, QUrl
from PyQt6.QtGui import QImage, QKeyEvent
from PyQt6.QtMultimedia import QSoundEffect
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout

from gui.common import CommonWidget
from gui.common.CommonObject import CommonObject
from gui.worker.ImageCaptureWorker import ImageCaptureWorker
from image import ImageCapture, ImageUtil, ImageEditor
import numpy as np
import os
import time

photo_shoot_sound_url = "./gui/sound/photo_shoot.wav"

NO_FRAME_IMAGE = -1
NO_OVERLAY = -1
FLIP_HORIZONTAL = True

class ImageCaptureWidget(CommonWidget):
    go_next = pyqtSignal()
    current_frame_image_index: int = NO_FRAME_IMAGE
    current_overlay_index: int = NO_OVERLAY
    save_image_path: str = None
    save_image = False

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

        self.image_util = ImageUtil()

        self.image_worker = ImageCaptureWorker(self)
        self.image_worker.setCallback(self.receiveImage)

        self.image_worker.start()

        self.image_editor = ImageEditor()
        self.image_util = ImageUtil()


    def startCapture(self):
        if self.data_manager.getSelectedFrame().overlayOnCam():
            self.current_overlay_index = 0
        else:
            self.current_overlay_index = -1
            self.current_frame_image_index = 0
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
        self.save_image_path = image_path
        self.save_image = True

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
                self.current_overlay_index = self.image_count
            else:
                self.current_frame_image_index = self.image_count
            return
        self.state_lb.setText(f"{self.count}초")
        self.count -= 1

    def __saveImage(self, img:np.ndarray):
        self.image_util.saveImage(self.save_image_path, img)
        self.data_manager.appendImage(img)
        self.save_image = False
        self.save_image_path = ""
        self.data_manager.appendShowImage(img)

    def __saveVideo(self, imageCapture:ImageCapture, img:np.ndarray):
        # current_time = time.time()
        # current_seconds = current_time - self.start_time
        # if current_seconds > self.count_second:
        #     self.save_video = False
        #     self.save_video_path = ""
        #     return
        pass

    def __flipImage(self, img:np.ndarray):
        return np.flip(img, 1)

    def __editOverlay(self, img:np.ndarray):
        """
        send image must be edited image
        and save image must be raw image
        :param img:
        :return:
        """
        canvas = img.copy()
        four_cut_data = self.data_manager.getSelectedFrame()
        overlay_img = four_cut_data.overlay_images[self.current_overlay_index]
        four_cut_photo_rect = four_cut_data.photo_rects[self.current_overlay_index].copy()
        overlay_relative_photo_rect = four_cut_data.getRelativeOverlayPhotoRect(self.current_overlay_index)
        edited_overly_img = self.image_editor.cutOverSizedOverlay(four_cut_photo_rect, overlay_relative_photo_rect, overlay_img)
        sized_up_ratio = self.image_editor.getSizeRatio(canvas, four_cut_photo_rect)
        overlay_relative_photo_rect.multiply(sized_up_ratio)
        canvas =  self.image_editor.cutWithRatio(canvas, four_cut_photo_rect)
        width = overlay_relative_photo_rect.getWidth()
        height = overlay_relative_photo_rect.getHeight()
        fixed_size_overlay_img = self.image_editor.resizeWithRatio(edited_overly_img, width, height)
        cut_image = self.image_editor.cutOverSize(fixed_size_overlay_img, width, height)
        self.image_editor.overwriteImage(canvas, cut_image, overlay_relative_photo_rect)
        return canvas

    def __editFrame(self, img:np.ndarray):
        canvas = img.copy()
        index = self.current_frame_image_index
        if index > 3:
            index = 3
        four_cut_data = self.data_manager.getSelectedFrame()
        four_cut_photo_rect = four_cut_data.photo_rects[index].copy()
        canvas = self.image_editor.cutWithRatio(canvas, four_cut_photo_rect)
        return canvas

    def receiveImage(self, img:np.ndarray):

        if FLIP_HORIZONTAL:
            img = self.__flipImage(img)
        if self.current_overlay_index != NO_OVERLAY:
            show_img = self.__editOverlay(img)
        elif self.current_frame_image_index != NO_FRAME_IMAGE:
            show_img = self.__editFrame(img)
        else:
            show_img = img

        self.setImage(self.image_util.cv2QImage(show_img))
        if self.save_image:
            self.__saveImage(img)


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


