import time

import numpy as np
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtGui import QImage

from gui.qt.src.common import CommonWidget
from gui.qt.src.test.gui_test_util import printOnlyOnce
from src.main.image import ImageCapture, ImageEditor, ImageUtil, FourCutData
from src.main.util import DataManager

NO_FRAME_IMAGE = -1
NO_OVERLAY = -1
FLIP_HORIZONTAL = True

class ImageCaptureWorker(QThread):
    imageCaptured = pyqtSignal(QImage)
    go:bool = True
    save_image:bool = False
    save_image_path:str = ""
    save_video:bool = False
    start_time = time.time()
    count_second:int = 0
    four_cut_data:FourCutData
    current_frame_image_index:int = NO_FRAME_IMAGE
    current_overlay_index:int = NO_OVERLAY

    def __init__(self, parent:CommonWidget=None):
        super().__init__()
        self.parent = parent
        self.data_manager:DataManager = parent.data_manager
        self.image_util = ImageUtil()
        self.image_editor = ImageEditor()
        self.imageCapture = ImageCapture()

    def saveImage(self, save_image_path:str):
        self.save_image_path = save_image_path
        self.save_image = True

    def saveVideo(self, save_video_path:str, seconds:int):
        self.save_video_path = save_video_path
        self.save_video = True
        self.start_time = time.time()
        self.count_second = seconds

    def setFourCutData(self, four_cut_data:FourCutData):
        self.four_cut_data = four_cut_data
        if self.four_cut_data.hasOverlayImages():
            self.current_overlay_index = 0

    def setCurrentOverlayIndex(self, overlay_index:int):
        self.current_overlay_index = overlay_index

    def setCurrentFrameImageIndex(self, frame_image_index:int):
        self.current_frame_image_index = frame_image_index

    def __saveImage(self, imageCapture:ImageCapture, img:np.ndarray):
        imageCapture.save_image(self.save_image_path, img)
        self.data_manager.appendImage(img)
        self.save_image = False
        self.save_image_path = ""

    def __saveVideo(self, imageCapture:ImageCapture, img:np.ndarray):
        current_time = time.time()
        current_seconds = current_time - self.start_time
        if current_seconds > self.count_second:
            self.save_video = False
            self.save_video_path = ""
            return

    def __flipImage(self, img:np.ndarray):
        return np.flip(img, 1)

    def __editOverlay(self, img:np.ndarray):
        canvas = img.copy()
        overlay_img = self.four_cut_data.overlay_images[self.current_overlay_index]
        four_cut_photo_rect = self.four_cut_data.photo_rects[self.current_overlay_index].copy()
        overlay_relative_photo_rect = self.four_cut_data.getRelativeOverlayPhotoRect(self.current_overlay_index)
        edited_overly_img = self.image_editor.cutOverSizedOverlay(four_cut_photo_rect, overlay_relative_photo_rect, overlay_img)
        sized_up_ratio = self.image_editor.getSizeRatio(canvas, four_cut_photo_rect)
        overlay_relative_photo_rect.multiply(sized_up_ratio)
        canvas =  self.image_editor.cutWithRatio(canvas, four_cut_photo_rect)
        width = overlay_relative_photo_rect.getWidth()
        height = overlay_relative_photo_rect.getHeight()
        fixed_size_overlay_img = self.image_editor.resizeWithRatio(edited_overly_img, width, height)
        cut_image = self.image_editor.cutOverSize(fixed_size_overlay_img, width, height)
        if self.save_image:
            self.__saveImage(self.imageCapture, canvas)
        self.image_editor.overwriteImage(canvas, cut_image, overlay_relative_photo_rect)
        qt_image = self.image_util.cv2QImage(canvas)
        self.imageCaptured.emit(qt_image)
        return canvas

    def stop(self):
        self.go = False

    def run(self):
        self.imageCapture.openCamera()
        while self.go:
            img = self.imageCapture.capture()
            if img is None:
                continue
            if FLIP_HORIZONTAL:
                img = self.__flipImage(img)
            if self.current_overlay_index != NO_OVERLAY:
                img = self.__editOverlay(img)
                continue
            if self.current_frame_image_index != NO_FRAME_IMAGE:
                four_cut_photo_rect = self.four_cut_data.photo_rects[self.current_overlay_index]
                img = self.image_editor.cutWithRatio(img,four_cut_photo_rect)

            qt_image = self.image_util.cv2QImage(img)
            self.imageCaptured.emit(qt_image)
            if self.save_image:
                self.__saveImage(self.imageCapture, img)
        self.imageCapture.closeCamera()







