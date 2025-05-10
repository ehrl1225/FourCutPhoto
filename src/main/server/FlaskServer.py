import sys

from flask import Flask, jsonify, request
from flask_socketio import SocketIO
from flask_cors import CORS
import base64
import os

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")
photo_path_list = []


@app.route('/', methods=['GET'])
def index():
    return 'Hello World!'

@app.route('/photo', methods=['PUT'])
def set_photo_urls():
    global photo_path_list
    photo_path_list.clear()
    data = request.get_json()
    url = data['url']

    for img_num in range(1,7):
        img_name = f"{img_num}.png"
        file_path = os.path.join(url, img_name)
        photo_path_list.append(file_path)
    # socketio.emit("photo_took",{"photo_took": True})
    return {
        "result": True
    }


@app.route('/photo', methods=['GET'])
def get_photo():
    photo_data_list = []
    for photo_path in photo_path_list:
        with open(photo_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            photo_data_list.append(encoded_string)
    return jsonify({"image": photo_data_list})

@app.route('/photo', methods=['POST'])
def select_photo():
    data = request.get_json()
    images = data['images']
    socketio.emit("photo_selected",{"selected_photos": images})
    return {
        "result": True
    }

@socketio.on('socket')
def clientProcess(message):
    print(message, flush=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8000, allow_unsafe_werkzeug=True)

