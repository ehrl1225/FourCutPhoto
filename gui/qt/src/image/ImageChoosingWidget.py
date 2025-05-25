from PyQt6.QtCore import pyqtSlot, Qt, pyqtSignal
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QGridLayout, QStackedLayout
from PyQt6.QtGui import QPixmap

from gui.qt.src.common.CommonObject import CommonObject
from src.main.image import ImageEditor, ImageUtil

class ImageChoosingWidget(QWidget):
    go_next = pyqtSignal()

    def __init__(self, parent:CommonObject=None):
        super().__init__()
        self.parent = parent
        self.data_manager = parent.data_manager
        self.selected_images = []  # Stores selected images and their order
        self.initUI()

    def initUI(self):
        # Create a grid layout to display images
        self.grid_layout = QGridLayout()

        # Create labels for images and add them to the grid

        # Create a layout for the main widget
        self.vbox = QVBoxLayout()

        self.vbox.addLayout(self.grid_layout)

        # Add an instruction label
        self.instruction_label = QLabel("사진을 4개 선택하세요", self)
        self.instruction_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.instruction_label.setStyleSheet("""
        font-size: 18px;
        height: 30px;
        """)
        self.vbox.addWidget(self.instruction_label)

        self.done_btn = QPushButton("다 선택했습니다.")
        self.done_btn.setStyleSheet("""
        font-size: 32px;
        height: 50px;
        """)

        self.vbox.addWidget(self.done_btn)
        self.vbox.addStretch(1)

        self.setLayout(self.vbox)
        self.setUI()

    def setUI(self):
        self.image_editor = ImageEditor()
        self.image_util = ImageUtil()

        self.done_btn.pressed.connect(self.setSelectedImages)

    def setSelectedImages(self):
        selected_frame = self.data_manager.getSelectedFrameIndex()
        four_cut_datas = self.data_manager.getFourCutDatas()[selected_frame]
        images = self.data_manager.getImages()
        selected_images = [images[i] for i in self.selected_images]
        edited_image = self.image_editor.editImage(four_cut_data=four_cut_datas, photos=selected_images)
        self.data_manager.saveImageDestination(edited_image)
        self.data_manager.setEditedImage(edited_image)
        self.selected_images.clear()
        for overlay in self.overlay_labels:
            overlay.setVisible(False)

        self.go_next.emit()

    def setImages(self):
        images = self.data_manager.images
        self.image_labels = []
        self.overlay_labels = []

        for i, image in enumerate(images):
            # Create a container widget for the image and overlay
            container = QWidget(self)
            container_layout = QStackedLayout(container)

            # Create the image label
            image_label = QLabel(container)
            pixmap = self.image_util.cv2QPixmap(image)
            image_label.setPixmap(pixmap.scaled(300, 300, Qt.AspectRatioMode.KeepAspectRatio))
            image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            # image_label.setStyleSheet("""
            # background-color: white;
            # """)
            image_label.mousePressEvent = lambda event, idx=i: self.select_image(idx)

            # Create the overlay label for the selection order
            overlay_label = QLabel(container)
            overlay_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            overlay_label.setStyleSheet(
                """
                background-color: #1e90ff;
                color: white;
                font-size: 32px;
                font-weight: bold;
                border-radius: 40px;
                padding: 10px;
                min-width: 50px;
                min-height: 80px;
                """
            )
            overlay_label.setVisible(False)  # Initially hidden

            self.image_labels.append(image_label)
            self.overlay_labels.append(overlay_label)

            # Add the image and overlay to the stacked layout
            container_layout.addWidget(image_label)
            container_layout.addWidget(overlay_label)

            # Add the container to the grid layout
            self.grid_layout.addWidget(container, i // 3, i % 3)

    def select_image(self, index):
        if index in self.selected_images:
            # If the image is already selected, deselect it
            self.selected_images.remove(index)
            self.overlay_labels[index].setVisible(False)  # Hide the overlay
        elif len(self.selected_images) < 4:
            # If less than 4 images are selected, add the image
            self.selected_images.append(index)

        # Update the overlay labels with the selection order
        for order, idx in enumerate(self.selected_images):
            self.overlay_labels[idx].setText(str(order + 1))  # Show the order
            self.overlay_labels[idx].setVisible(True)

        # Update the instruction label
        if len(self.selected_images) == 4:
            self.instruction_label.setText("4개의 사진을 선택했습니다.")
        else:
            self.instruction_label.setText(f"사진을 {4 - len(self.selected_images)}개 더 선택하세요.")


