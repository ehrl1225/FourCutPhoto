from PyQt6.QtCore import QThread, pyqtSignal
import socketio

class SocketWorker(QThread):
    server_ip:str = "ws://localhost:8000"
    sio:socketio.Client
    take_photo = pyqtSignal()
    recode_video = pyqtSignal(int)
    photo_selected = pyqtSignal(list)
    go:bool=True

    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.sio = socketio.Client()

    def run(self):
        self.sio.connect(url="ws://localhost:8000")
        @self.sio.event
        def connect():
            print("connected to server")

        @self.sio.event
        def disconnect():
            print("disconnected from server")

        @self.sio.on('photo')
        def take_photo():
            self.take_photo.emit()

        @self.sio.on('photo_selected')
        def photo_selected_received(data):
            selected_photos = data['selected_photos']
            print("received photo from server")
            self.photo_selected.emit(selected_photos)
        while self.go:
            self.sio.wait()
        self.sio.disconnect()
