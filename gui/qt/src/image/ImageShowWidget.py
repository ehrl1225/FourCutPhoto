from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QVBoxLayout, QGridLayout, QHBoxLayout, QPushButton, QLabel

from gui.qt.src.common import CommonImageWidget, CommonWidget
from src.main.image import ImageUtil, ImageEditor
from src.main.util import DataManager


class ImageShowWidget(CommonImageWidget):
    go_back = pyqtSignal()
    go_next = pyqtSignal()

    def __init__(self, parent:CommonWidget=None):
        super().__init__()
        self.data_manager:DataManager = parent.data_manager
        self.initUI()

    def initUI(self):
        self.grid_layout = QGridLayout()

        vbox = QVBoxLayout()
        vbox.addLayout(self.grid_layout)

        self.go_back_btn = QPushButton("돌아가기")
        self.go_next_btn = QPushButton("확인")

        btn_hbox = QHBoxLayout()
        btn_hbox.addWidget(self.go_back_btn)
        btn_hbox.addWidget(self.go_next_btn)

        vbox.addLayout(btn_hbox)
        vbox.addStretch(1)

        self.image_util = ImageUtil()
        self.image_editor = ImageEditor()

        self.setLayout(vbox)
        self.setUI()

    def setUI(self):
        self.go_back_btn.pressed.connect(self.goBack)
        self.go_next_btn.pressed.connect(self.goNext)

    def setImages(self):
        images = self.data_manager.getImages()
        self.image_labels = []
        four_cut_data = self.data_manager.getSelectedFrame()
        for i, image in enumerate(images):
            canvas = image.copy()
            overlay_img = four_cut_data.overlay_images[i]
            four_cut_photo_rect = four_cut_data.photo_rects[i].copy()
            overlay_relative_photo_rect = four_cut_data.getRelativeOverlayPhotoRect(i)
            sized_up_ratio = self.image_editor.getSizeRatio(canvas, four_cut_photo_rect)
            overlay_relative_photo_rect.multiply(sized_up_ratio)
            canvas = self.image_editor.cutWithRatio(canvas, four_cut_photo_rect)
            width = overlay_relative_photo_rect.getWidth()
            height = overlay_relative_photo_rect.getHeight()
            fixed_size_overlay_img = self.image_editor.resizeWithRatio(overlay_img, width, height)
            cut_image = self.image_editor.cutOverSize(fixed_size_overlay_img, width, height)
            print(width, height)
            self.image_editor.overwriteImage(canvas, cut_image, overlay_relative_photo_rect)
            edited_pixmap = self.image_util.cv2QPixmap(canvas)
            image_label = QLabel(self)
            image_label.setPixmap(edited_pixmap)
            image_label.resize(300, 300)
            image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.grid_layout.addWidget(image_label, i//2, i%2)

    def editImage(self):
        selected_frame = self.data_manager.getSelectedFrame()
        images = self.data_manager.getImages()
        edited_image = self.image_editor.editImage(four_cut_data=selected_frame, photos=images)
        self.data_manager.saveImageDestination(edited_image)
        self.data_manager.setEditedImage(edited_image)


    def goNext(self):
        self.editImage()
        self.go_next.emit()

    def goBack(self):
        self.go_back.emit()