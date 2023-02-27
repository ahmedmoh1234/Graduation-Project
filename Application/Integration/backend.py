from flask import Flask, jsonify, request
import jwt
import cv2
import numpy as np
import matplotlib.pyplot as plt
import skimage
from PIL import Image
from Face_Recognition.test import FaceDetector
from Emotion_Recognition.main import emoDetection
import os

# Run ipconfig in command prompt to get IP Address
IP_ADDRESS = '192.168.1.22'

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



@app.route('/face-detector', methods=['POST'])
def face_detector():   
    try:
        file = request.files['image']

    except:
        print('No image')
        return 'No image'
    img = cv2.imdecode(np.fromstring(file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
    print(img.shape)
    PILImage = Image.open(file.stream)
    PILImage.show()
    fd = FaceDetector()
    result = fd.faceMatch(PILImage, 1)
    print(f"Faced matched with {result}")
    # response = dict()
    # response['result'] = result
    # return jsonify(response)
    return result

@app.route('/emotion-recognizer', methods=['POST'])
def emotion_recognizer():    
    file = request.files['image']
    img = cv2.imdecode(np.fromstring(file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
    print(img.shape)
    # PILImage = Image.open(file.stream)
    # PILImage.show()
    img, result = emoDetection(img)
    return result
    


if __name__ == "__main__":
    app.run(debug = True, host = IP_ADDRESS)