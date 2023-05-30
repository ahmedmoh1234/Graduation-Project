from ultralytics import YOLO
import torch
import numpy as np
import os
import cv2
import sys
from pathlib import Path
# sys.path.insert(0, os.path.dirname(__file__))

FILE = Path(__file__).resolve()
# print(50*'-')
# print(f'{FILE.parents[0]}\{model_path}')
# print(50*'-')


class BrandRecognition:

    model : YOLO = None 

    def __init__(self, model_path):
        self.model = YOLO(f'{FILE.parents[0]}\{model_path}')

    def predict(self, img)-> str:

        if self.model is None:
            return "Model not loaded"
        
        results = self.model.predict(img)

        if len(results[0].boxes) == 0:
            return "No logo detected"
        
        box = results[0].boxes[0]

        names_dict = results[0].names

        return names_dict[box.cls.item()]
    
class ProductDetection():
    model = None

    def __init__(self, model_path):
        model = torch.hub.load('ultralytics/yolov5', 'custom', path=f'{FILE.parents[0]}\{model_path}', trust_repo=True)
        self.model = model

    def predict(self, img) ->tuple[list[np.ndarray],str] : # returns a tuple of a list of images and a string of the product name
        if self.model is None:
            return "Model not loaded"
        
        results = self.model(img)

        names_dict = results.names
        #Since we only passed one image, we only need the first element of the list
        print(results.pandas().xyxy[0])

        foundObjects = []

        for i in range(len(results.pandas().xyxy[0])):
            if results.pandas().xyxy[0].iloc[i]['confidence'] < 0.5:
                continue
            #crop the image
            box = results.pandas().xyxy[0].iloc[i]
            cropped_img = img[int(box.ymin):int(box.ymax), int(box.xmin):int(box.xmax)]
            foundObjects.append((cropped_img,names_dict[box['class']]))
            # print('Box: ', end = '') 
            # print(box['class'])
            
        #Display the found objects
        # for i in range(len(foundObjects)):
        #     cv2.imshow("Object " + str(i), foundObjects[i])
        #     cv2.waitKey(0) 

        return foundObjects


if __name__ == "__main__":
    img = cv2.imread("5.jpg")
    pd = ProductDetection('product_detect.pt')
    foundObjects = pd.predict(img)
    br = BrandRecognition('logo_detect.pt')
    finalStr = ""
    for i in range(len(foundObjects)):
        finalStr += foundObjects[i][1] + ", " + br.predict(foundObjects[i][0]) + "\n"
    
    print(finalStr)
    


    
    

