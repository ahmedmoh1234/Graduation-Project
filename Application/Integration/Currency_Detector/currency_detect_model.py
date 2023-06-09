from matplotlib import pyplot as plt
import os
# from playsound import playsound
import cv2
import subprocess
from gtts import gTTS
import os
import sys
import pathlib
PATH = pathlib.Path(__file__).parent
from ultralytics import YOLO



sys.path.insert(0, os.path.dirname(__file__))
# print(50*'-')
# print(sys.path)
# print(50*'-')
from currency_utils import resize_img
# from utils import *

def createAbsolutePaths(relativePath):
    absPath = os.path.dirname(__file__)
    absPath = absPath.replace('\\', '/')
    absPath = absPath + relativePath
    return absPath



def currency_detector_ready(currencyImg):
	max_val = 8
	max_pt = -1
	max_kp = 0

	orb = cv2.ORB_create()
	# orb is an alternative to SIFT
	test_img = currencyImg

	# r = YOLO('trained-model/train2/weights/epoch3.pt').predict('preprocessed-data/test/images/796856579.jpg')
	r = YOLO(PATH/'trained-model/train2/weights/best.pt').predict(currencyImg)
	class_names = ['5egp', '10egp', '20egp', '50egp', '100egp', '200egp']

	currency = r[0].boxes.cls
	currency = [class_names[int(i)] for i in currency]
	print(currency)
	if len(currency) == 0:
		return 'None'
	#cut the string to get the number only
	currency = currency[0].split('egp')[0]
	return 'this is a ' + currency + ' pounds note'
	# resizing must be dynamic
	# original = resize_img(test_img, 0.4)
	# original = test_img
	# display('original', original)



# currency_detector_ready(cv2.imread(createAbsolutePaths('/100LE_1.jpg')))