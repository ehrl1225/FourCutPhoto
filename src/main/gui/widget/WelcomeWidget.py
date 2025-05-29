from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QStackedLayout, QGraphicsProxyWidget, QHBoxLayout
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, pyqtSignal


class WelcomeWidget(QWidget):
    go_next = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__()
        self.initUI()

    def initUI(self):
        # self.welcome_label = QLabel("빛울림의 밤에 오신걸 환영합니다", self)
        # self.welcome_label.setStyleSheet("font-size: 24px; color: white;")
        self.background_label = QLabel(self)
        pixmap = QPixmap("gui/img/welcome_img.png")
        screen_size = self.screen().size()
        width = screen_size.width()
        height = screen_size.height()
        pixmap = pixmap.scaled(width, height, Qt.AspectRatioMode.KeepAspectRatio)
        self.background_label.resize(width, height)
        self.background_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.background_label.setPixmap(pixmap)
        self.background_label.setScaledContents(True)

        hbox = QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(self.background_label)
        hbox.addStretch()


        self.start_button = QPushButton(self)
        self.start_button.setStyleSheet("""
                                        background-color: transparent;  /* 버튼 배경 투명 */
                                        border: none;  /* 테두리 제거 */
                                        color: black;  /* 텍스트 색상 */
                                        """)
        
        self.start_button.setGeometry(600, 290, 290, 100)

        # welcome_layout = QVBoxLayout()
        # welcome_layout.addWidget(self.welcome_label)
        # welcome_layout.addWidget(self.start_button)
        # welcome_layout.setAlignment(self.welcome_label, Qt.AlignmentFlag.AlignCenter)
        # welcome_layout.setAlignment(self.start_button, Qt.AlignmentFlag.AlignCenter)

        self.setLayout(hbox)

        self.setUI()

    def setUI(self):
        self.start_button.pressed.connect(self.onStartPress)

    def onStartPress(self):
        self.go_next.emit()