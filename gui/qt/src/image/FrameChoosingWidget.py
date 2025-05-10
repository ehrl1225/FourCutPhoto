from functools import partial

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QButtonGroup, QRadioButton
from PyQt6.QtGui import QPixmap, QImage

from gui.qt.src.common.CommonObject import CommonObject
from gui.qt.src.custom_widget.ClickableLabel import ClickableLabel
from src.main.image import ImageUtil, ImageEditor


class FrameChoosingWidget(QWidget):
    go_next = pyqtSignal()

    def __init__(self, parent:CommonObject=None):
        super().__init__()
        self.parent = parent
        self.data_manager = parent.data_manager
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Create a horizontal layout to hold the images and radio buttons
        image_layout = QHBoxLayout()

        # Button group to manage radio buttons
        self.image_lb_list = list()

        self.button_group = QButtonGroup()

        for i in range(4):
            # Create a vertical layout for each image and its radio button
            vbox = QVBoxLayout()

            # Create and set the image label
            label = ClickableLabel(self)
            self.image_lb_list.append(label)
            label.clicked.connect(partial(self.check_image, i))

            vbox.addWidget(label, 1)

            # Create and add the radio button
            radio_button = QRadioButton(f"Image {i+1}")
            radio_button.setStyleSheet("""
            font-size: 18px;
            """)
            self.button_group.addButton(radio_button, i)
            vbox.addWidget(radio_button)

            # Add the vertical layout to the horizontal layout
            image_layout.addLayout(vbox)

        # Add the image layout to the main layout
        layout.addLayout(image_layout)

        # Add a button to confirm the selection
        select_button = QPushButton("이미지 선택 완료", self)
        select_button.setStyleSheet("""
        font-size: 32px; 
        height: 100px;
        """)
        select_button.clicked.connect(self.select_image)
        layout.addStretch(1)
        layout.addWidget(select_button)
        layout.addStretch(1)

        self.setLayout(layout)
        self.setUI()

    def setUI(self):
        self.image_util = ImageUtil()
        self.image_editor = ImageEditor()

    def setImages(self):
        four_cut_datas = self.data_manager.getFourCutDatas()
        width = 200
        height = 500
        for index, four_cut_data in enumerate(four_cut_datas):
            photo = four_cut_data.photo
            resized_photo =  self.image_editor.resizeWithRatio(photo, width, height)
            qt_image:QPixmap = self.image_util.cv2QPixmap(resized_photo)
            self.image_lb_list[index].setPixmap(qt_image)
            self.image_lb_list[index].resize(width, height)

    def check_image(self, index):
        self.button_group.button(index).setChecked(True)

    def select_image(self):
        selected_id = self.button_group.checkedId()
        if selected_id != -1:
            self.data_manager.setSelectedFrameIndex(selected_id)
        else:
            return
        self.button_group.button(selected_id).setChecked(False)
        self.go_next.emit()