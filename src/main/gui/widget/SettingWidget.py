from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider, QHBoxLayout, QComboBox, QPushButton
from gui.common.CommonObject import CommonObject
from printer.Printer import Printer


class SettingWidget(QWidget):

    def __init__(self, parent:CommonObject=None):
        super().__init__()
        self.parent = parent
        self.data_manager = parent.data_manager
        self.initUI()

    def initUI(self):

        self.frame_width_lb = QLabel('Frame Width')
        self.frame_height_lb = QLabel('Frame Height')
        self.frame_width_slider = QSlider(Qt.Orientation.Horizontal)
        self.frame_height_slider = QSlider(Qt.Orientation.Horizontal)

        self.image_width_lb = QLabel('Image Width')
        self.image_height_lb = QLabel('Image Height')
        self.image_width_slider = QSlider(Qt.Orientation.Horizontal)
        self.image_height_slider = QSlider(Qt.Orientation.Horizontal)

        self.printer_text_cb = QComboBox()
        self.printer_select_btn = QPushButton('Select Printer')

        hbox = QHBoxLayout()
        hbox.addWidget(self.printer_text_cb)
        hbox.addWidget(self.printer_select_btn)


        vbox = QVBoxLayout()

        # vbox.addWidget(self.frame_width_lb)
        # vbox.addWidget(self.frame_width_slider)
        # vbox.addWidget(self.frame_height_lb)
        # vbox.addWidget(self.frame_height_slider)
        #
        # vbox.addWidget(self.image_width_lb)
        # vbox.addWidget(self.image_width_slider)
        # vbox.addWidget(self.image_height_lb)
        # vbox.addWidget(self.image_height_slider)

        # vbox.addWidget(self.printer_text_list)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

    def setUI(self):
        self.printer = Printer()
        names = self.printer.get_printers()
        self.printer_text_list.clear()
        for name in names:
            self.printer_text_list.addItem(name)
