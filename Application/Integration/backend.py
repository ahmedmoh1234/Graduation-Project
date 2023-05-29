from flask import Flask, jsonify, request
import jwt
import cv2
import numpy as np
import matplotlib.pyplot as plt
import skimage
import os
import time
from PIL import Image
import getmac
import logging

from Face_Recognition.test import FaceDetector
from Emotion_Recognition.main import  loadEmoDetector
from Scene_Descriptor.Scene_Descriptor import SceneDescriptor
from Clothes_Descriptor.Clothes_Description import describe_clothes
from Currency_Detector.currency_detect import currency_detector
from Document_scanner.main import document_scanner
from Product_Identifier.product_detect import ProductDetection, BrandRecognition
# from Currency_Detector.detect import currency_detector
from Apparel_recom.apparel import ApparelRecommender




# Run ipconfig in command prompt to get IP Address
IP_ADDRESS = '192.168.1.7'
# IP_ADDRESS = 'localhost'

logging.basicConfig(filename='logs.log', level=logging.DEBUG)

app = Flask(__name__)

pd = ProductDetection('product_detect.pt')
br = BrandRecognition('logo_detect.pt')
emoDetector = loadEmoDetector()
sceneDescriptor = SceneDescriptor("./Scene_Descriptor/weights/yolov8s-seg.pt")



ar = ApparelRecommender()



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
    response = sceneDescriptor.estimate_depth(img)
    # print(img.shape)
    # PILImage = Image.open(file.stream)
    # PILImage.show()
    # print(f"Scene Descriptor: {response}")
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
    # img = cv2.imdecode(np.fromstring(file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
    # print(img.shape)
    PILImage = Image.open(file.stream)
    # PILImage.show()
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
    # print(img.shape)
    # PILImage = Image.open(file.stream)
    # PILImage.show()
    img, result = emoDetector.executeWithImage(img)
    # print(f"Emotion: {result[0]}")
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
    
@app.route('/document-reader', methods=['POST'])
def document_reader():    
    file = request.files['image']
    img = cv2.imdecode(np.fromstring(file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
    # PILImage = Image.open(file.stream)
    # print(img.shape)
    # PILImage.show()
    result = document_scanner(img)
    return result

@app.route('/product-identifier', methods=['POST'])
def product_identifier():    
    global pd
    global br
    file = request.files['image']
    img = cv2.imdecode(np.fromstring(file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
    # PILImage = Image.open(file.stream)
    # print(img.shape)
    # PILImage.show()
    product = {"soda can":["pepsi","coca cola"],
               "water bottle" : ["nestle", "aquafina"],
               "No logo detected" : ["no logo detected"]}
    foundObjects = pd.predict(img)
    finalStr = ""
    for i in range(len(foundObjects)):
        finalStr += foundObjects[i][1]
        if finalStr == "":
            finalStr = "No products found"
            return finalStr
        finalStr += " , "
        temp = br.predict(img)
        if temp in product[foundObjects[i][1]]:
            finalStr += temp
        else:
            finalStr += "no logo detected"

    if finalStr == "":
        finalStr = "No products found"
    return finalStr

@app.route('/apparel', methods=['POST'])
def apparel():    

    #Get mac address

    ip_addr = request.environ.get('REMOTE_ADDR')
    mac_addr = getmac.get_mac_address(ip=ip_addr)
    if ip_addr == '127.0.0.1': #localhost
        logging.info("User is localhost")
        mac_addr = getmac.get_mac_address() #get mac address of the server
    
    #Load the model using the mac address
    createModel = False
    if ar.loadUserPreference(mac_addr):
        logging.info("Model loaded")
    else:
        logging.info("Model not loaded")
        createModel = True
        

    texture = request.json['texture']
    color = request.json['color']
    clothesType = request.json['clothesType']
    

    prodId = ar.getProductID(texture, color, clothesType)


    if prodId[0] == -1:
        #This means that this is a new product
        #Add it to the database
        logging.info("New product. Adding to database")
        ar.addApparelData(prodId[1], texture, color, clothesType)
        result = ar.getTopRecommendations(prodId[1], 1)
        if isinstance(result, str):
            result = result
        else:
            #only return the texture, color and clothes type
            resultStr = "We recommend the "
            resultStr += str(result['color'].iloc[0]) + ", " + str(result['texture'].iloc[0]) +   " " + str(result['clothes_type'].iloc[0])
            result = resultStr

    elif prodId[0] == -2:
        #This means that the database is empty
        #Add it to the database
        logging.info("Database is empty. Adding to database")
        ar.addApparelData(prodId[1], texture, color, clothesType)
        result = "There isn't enough data to make a recommendation"

    else:
        #This means that the product is already in the database
        logging.info("Product already in database")
        result = ar.getTopRecommendations(prodId[0], 1)
        if isinstance(result, str):
            result = result
        else:
            resultStr = "We recommend the "
            resultStr += str(result['color'].iloc[0]) + ", " + str(result['texture'].iloc[0]) +   " " + str(result['clothes_type'].iloc[0])
            result = resultStr
    
    if createModel:
        logging.info("Saving model")
        ar.saveUserPreference(mac_addr)

    return result


if __name__ == "__main__":
    app.run(debug = True, host = IP_ADDRESS)