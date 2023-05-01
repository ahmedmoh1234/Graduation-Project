from flask import Flask, jsonify, request
import jwt
import cv2
import numpy as np
import matplotlib.pyplot as plt
import skimage
from PIL import Image
from Face_Recognition.test import FaceDetector
from Emotion_Recognition.main import emoDetection
from Scene_Descriptor.Scene_Descriptor import detect_obj
from Clothes_Descriptor.Clothes_Description import describe_clothes
from Currency_Detector.currency_detect import currency_detector

# from Currency_Detector.detect import currency_detector
import os

# Run ipconfig in command prompt to get IP Address
IP_ADDRESS = '192.168.1.3'

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
    response = detect_obj(img)
    PILImage = Image.open(file.stream)
    PILImage.show()
    print(f"Scene Descriptor: {response}")
    return response


@app.route('/clothes-descriptor', methods=['POST'])
def clothes_descriptor():    
    file = request.files['image']
    img = cv2.imdecode(np.fromstring(file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
    print(img.shape)
    response = describe_clothes(img)
    PILImage = Image.open(file.stream)
    PILImage.show()
    print(f"Clothes Descriptor: {response}")
    return response

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
    PILImage = Image.open(file.stream)
    PILImage.show()
    img, result = emoDetection(img)
    print(f"Emotion: {result[0]}")
    return result[0]


@app.route('/currency-recognizer', methods=['POST'])
def currency_recognizer():    
    file = request.files['image']
    img = cv2.imdecode(np.fromstring(file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
    # PILImage = Image.open(file.stream)
    # print(img.shape)
    # PILImage.show()
    # img = cv2.imread('20LE_1.jpg')
    result = currency_detector(img)
    print()
    return result
    


if __name__ == "__main__":
    app.run(debug = True, host = IP_ADDRESS)