from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt, pyqtSignal

from gui.common import CommonWidget


class SelectPeopleNumberWidget(CommonWidget):
    go_next = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__()
        self.data_manager = parent.data_manager
        self.initUI()

    def initUI(self):
        self.people_count = 1  # Default number of people

        self.background_label = QLabel(self)
        pixmap = QPixmap("gui/img/select_img.png")
        screen_size = self.screen().size()
        width = screen_size.width()
        height = screen_size.height()
        pixmap = pixmap.scaled(width, height, Qt.AspectRatioMode.KeepAspectRatio)
        self.background_label.setPixmap(pixmap)
        self.background_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.background_label.setScaledContents(True)

        # Create label to display the number of people
        self.people_label = QLabel(f"{self.people_count} 명", self)
        self.people_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.people_label.setStyleSheet("""
                                        font-size: 32px;
                                        font-weight: bold;
                                        background-color : white;
                                        color : black
                                        """)
        self.people_label.setGeometry(640, 315, 200, 100)

        # Create left and right buttons to adjust the number of people
        self.left_button = QPushButton(self)
        self.left_button.setStyleSheet("""
        background-color : transparent;
        """)
        self.left_button.clicked.connect(self.decrease_people_count)
        self.left_button.setGeometry(500, 300, 130, 115)

        self.right_button = QPushButton(self)
        self.right_button.setStyleSheet("""
        background-color : transparent;
        
        """)
        self.right_button.clicked.connect(self.increase_people_count)
        self.right_button.setGeometry(860, 310, 130, 115)

        # Create a layout for the buttons and label
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.left_button)
        button_layout.addWidget(self.people_label)
        button_layout.addWidget(self.right_button)
        button_layout.addStretch()

        # Create the next button
        self.next_button = QPushButton("다음", self)
        self.next_button.setStyleSheet("""
        font-size: 32px;
        font-weight: bold;
        color : black;
        background-color : white;
        """)
        self.next_button.setGeometry(1100, 400, 350, 100)

        # Create a label to instruct the user to press the next button
        self.instruction_label = QLabel("다음 버튼을 눌러 주세요", self)
        self.instruction_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.instruction_label.setStyleSheet("""
        font-size: 32px;
        font-weight: bold;
        background-color : white;
        border-radius: 50px;
        color : black;
        """)
        self.instruction_label.setGeometry(1100, 200, 350, 100)

        # Create the main layout
        # main_layout = QHBoxLayout(self)
        # main_layout.addLayout(button_layout)
        # main_layout.addWidget(self.next_button)
        # main_layout.addWidget(self.instruction_label)

        hbox = QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(self.background_label)
        hbox.addStretch()


        self.setLayout(hbox)
        self.setUI()

    def setUI(self):
        self.next_button.clicked.connect(self.next_step)

    def decrease_people_count(self):
        if self.people_count > 1:
            self.people_count -= 1
            self.people_label.setText(f"{self.people_count} 명")

    def increase_people_count(self):
        self.people_count += 1
        self.people_label.setText(f"{self.people_count} 명")

    def next_step(self):
        self.data_manager.setPeopleCount(self.people_count)
        self.go_next.emit()