import cv2
from time import sleep
import requests
import io
import json
import os
import random
#import tessaract
import pytesseract
from PIL import Image
import copy
import pathlib
PATH = pathlib.Path(__file__).parent

def document_tesseract(img):
    

    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    # image_path = "image.jpg"
    # img = Image.open(image_path)
    print(type(img))
    # i = cv2.imread(image_path)
    # print(type(i))
    text = pytesseract.image_to_string(img)
    print("Extracted text:\n", text)
    return text