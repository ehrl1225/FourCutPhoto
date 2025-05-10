import socketio

sio = socketio.Client()

@sio.event
def connect():
    print('connected')

@sio.on('socket')
def clientProcess(message):
    sio.emit('socket', {'commond':"test"})

if __name__ == '__main__':
    sio.connect("ws://127.0.0.1:8000")
    sio.emit("socket", {"command":"test"})
    sio.wait()

