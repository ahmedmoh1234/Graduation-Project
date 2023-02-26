from flask import Flask, jsonify, request
import jwt
import cv2
import numpy as np
import matplotlib.pyplot as plt
import skimage
from PIL import Image


# Run ipconfig in command prompt to get IP Address
IP_ADDRESS = '192.168.1.8'

app = Flask(__name__)


@app.route('/test', methods=['POST'])
def test():
    print('Test')
    return 'test'

@app.route('/command', methods=['POST'])
def command():
    data = request.json
    command = data['command']
    print(command)
    return 'Success'


@app.route('/scene-descriptor', methods=['POST'])
def scene_descriptor():    
    file = request.files['image']
    img = cv2.imdecode(np.fromstring(file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
    print(img.shape)
    PILImage = Image.open(file.stream)
    PILImage.show()
    return 'Success'

if __name__ == "__main__":
    app.run(debug = True, host = IP_ADDRESS)