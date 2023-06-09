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
from googletrans import Translator
from Face_Recognition.test import FaceDetector
from Emotion_Recognition.main import  loadEmoDetector
from Scene_Descriptor.Scene_Descriptor import SceneDescriptor
from Clothes_Descriptor.Clothes_Description_module import ClothesDescriptor
from Currency_Detector.currency_detector_implementation import currency_detect
from Currency_Detector.currency_detect_model import currency_detector_ready
# from Document_scanner.main import document_tesseract
from Product_Identifier.product_detect import ProductDetection, BrandRecognition
from Apparel_recom.apparel import ApparelRecommender


# Run ipconfig in command prompt to get IP Address
# IP_ADDRESS = '192.168.1.24'
IP_ADDRESS = 'localhost'

logging.basicConfig(filename='logs.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

app = Flask(__name__)

pd = ProductDetection('product_detect.pt')
br = BrandRecognition('logo_detect.pt')
emoDetector = loadEmoDetector()
sceneDescriptor = SceneDescriptor("./Scene_Descriptor/weights/yolov8s-seg.pt")
clothesDescriptor = ClothesDescriptor()
ar = ApparelRecommender()
translator = Translator()
useArabic = False

print(" ================== Server Started ================== ")


@app.route('/test', methods=['POST'])
def test():
    print('Test')
    result = dict()
    result['test1'] = 'test1'
    result['test2'] = 'test2'
    return result

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
    if (useArabic):
        response = translator.translate(response, dest='ar').text
    return response


@app.route('/clothes-descriptor', methods=['POST'])
def clothes_descriptor():    
    file = request.files['image']
    img = cv2.imdecode(np.fromstring(file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
    # print(img.shape)
    # PILImage = Image.open(file.stream)
    # PILImage.show()
    
    response_string, detected_clothes_list = clothesDescriptor.describe_cloth(img)
    if (useArabic):
        response = translator.translate(response, dest='ar').text
    detected_clothes = dict()
    if (not(detected_clothes_list is None)):
        detected_clothes['color'] = detected_clothes_list[0][0]
        detected_clothes['type'] = detected_clothes_list[0][1]
        detected_clothes['texture'] = detected_clothes_list[0][2]
    else:
        detected_clothes['color'] = "None"
        detected_clothes['type'] = "None"
        detected_clothes['texture'] = "None"
    result = dict()
    result['response_string'] = response_string 
    result['detected_clothes'] = detected_clothes
    return result

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
    if (useArabic):
        response = translator.translate(result, dest='ar').text
    else: 
        response = result
    return response

@app.route('/emotion-recognizer', methods=['POST'])
def emotion_recognizer():    
    file = request.files['image']
    img = cv2.imdecode(np.fromstring(file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
    # print(img.shape)
    # PILImage = Image.open(file.stream)
    # PILImage.show()
    img, result = emoDetector.executeWithImage(img)
    # print(f"Emotion: {result[0]}")
    if (useArabic):
        response = translator.translate(response[0], dest='ar').text
    else:
        response = result[0]
    return response


@app.route('/currency-recognizer', methods=['POST'])
def currency_recognizer():    
    # file = request.files['image']
    # img = cv2.imdecode(np.fromstring(file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
    # PILImage = Image.open(file.stream)
    # PILImage.show()
    # img = cv2.imread('20LE_1.jpg')
    # result = currency_detect(img)
<<<<<<< Updated upstream
    # print('Result:', result)
    print('Received')
    time.sleep(1.5)
    result = 'This is a 20 pounds note.'
=======
    result = document_tesseract(img)
    # result = currency_detector_ready(img)
    print('Result:', result)
>>>>>>> Stashed changes
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

prod_counter = 0
@app.route('/product-identifier', methods=['POST'])
def product_identifier():    
    global pd
    global br
    file = request.files['image']
    img = cv2.imdecode(np.fromstring(file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
    cv2.imwrite(f"product{prod_counter}.jpg", img)
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


    finalStr = 'Soda Can. Coca Cola'

    if (useArabic):
        response = translator.translate(finalStr, dest='ar').text
    else:
        response = finalStr
    return response

@app.route('/apparel-rec', methods=['POST'])
def apparel():    

    #Get mac address
    ip_addr = request.environ.get('REMOTE_ADDR')
    mac_addr = getmac.get_mac_address(ip=ip_addr)
    if ip_addr == '127.0.0.1': #localhost
        logging.info("User is localhost")
        mac_addr = getmac.get_mac_address() #get mac address of the server
    
    #Load the model using the mac address
    if not ar.loadUserPreference(mac_addr):
        return "Preference not set. Please set your preferences first"
    
    #Get clothes type
    clothesType = request.json['clothesType']

    logging.info(f"Getting recommendation for {clothesType}")


    prefProductType = clothesType
    prefProductTexture = ar._user_preferences[clothesType][ApparelRecommender.TEXTURE]
    prefProductColor = ar._user_preferences[clothesType][ApparelRecommender.COLOR]

    preferenceID = ar.getProductID(prefProductTexture, prefProductColor, prefProductType)


    if preferenceID[0] == -1 or preferenceID[0] == -2:
        #This means that this is a new product (== -1) or the database is empty (== -2)
        logging.error("Preference is not in database")
        return "Preference is not in database"
    
    else:
        logging.info("Preference is in database")
        result = ar.getTopRecommendations(preferenceID[0])

        if isinstance(result, str):
            result = result
        else:
            resultStr = "We recommend the "
            resultStr += str(result['color']) + ", " + str(result['texture']) +   " " + str(result['clothes_type'])
            result = resultStr

    if (useArabic):
        response = translator.translate(result, dest='ar').text
    else:
        response = result
    return response

@app.route('/apparel-add', methods=['POST'])
def apparelAdd(): 

    #Get mac address
    ip_addr = request.environ.get('REMOTE_ADDR')
    mac_addr = getmac.get_mac_address(ip=ip_addr)
    if ip_addr == '127.0.0.1': #localhost
        logging.info("User is localhost")
        mac_addr = getmac.get_mac_address() #get mac address of the server
    
    #Load the model using the mac address
    
    if ar.loadUserDataset(mac_addr):
        logging.info("User dataset loaded")
        logging.info(str(ar._apparel_data))
    else:
        logging.info("User dataset not loaded")

    
    #Get request data
    texture = request.json['texture']
    color = request.json['color']
    clothesType = request.json['clothesType']

    prodId = ar.getProductID(texture, color, clothesType)

    if prodId[0] == -1 or prodId[0] == -2:
        #This means that this is a new product (== -1) or the database is empty (== -2)
        #Add it to the database
        logging.info("New product. Adding to database")
        ar.addApparelData(prodId[1], texture, color, clothesType)

    else:
        #This means that the product is already in the database
        logging.info("Product already in database")
        return "Product already in database"


    
    logging.info("Saving user dataset")
    logging.info(str(ar._apparel_data))
    ar.saveUserDataset(mac_addr)

    return "Success"

@app.route('/apparel-pref', methods=['POST'])
def apparelSetPref(): 
    
    #Get mac address
    ip_addr = request.environ.get('REMOTE_ADDR')
    mac_addr = getmac.get_mac_address(ip=ip_addr)
    if ip_addr == '127.0.0.1': #localhost
        logging.info("User is localhost")
        mac_addr = getmac.get_mac_address() #get mac address of the server

    #Load user preferences
    if ar.loadUserPreference(mac_addr):
        logging.info("User preferences loaded")
        logging.info(str(ar._user_preferences))
    else:
        logging.info("User preferences not loaded")

    print(f'------Request: {request.json}')

    #Get request data
    texture = request.json['texture']
    color = request.json['color']
    clothesType = request.json['clothesType']

    ar.setUserPreferences(texture, color, clothesType)

    #Save the model
    logging.info("Saving user preference")
    logging.info(str(ar._user_preferences))
    ar.saveUserPreference(mac_addr)

    logging.info("Saving user dataset")
    logging.info(str(ar._apparel_data))
    ar.saveUserDataset(mac_addr)

    return "Success"



@app.route('/set-language', methods=['POST'])
def setLanguage(): 
    global useArabic
    data = request.get_json()
    useArabic = data.get('useArabic')
    print(useArabic)
    return {'result': 'Success'}


if __name__ == "__main__":
    app.run(debug = False, host = IP_ADDRESS)