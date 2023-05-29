from ultralytics import YOLO
import numpy as np
import inflect
import os
import pickle
import cv2
from matplotlib import pyplot as plt

class ClothesDescriptor():
    
    def __init__(self):
        self.p = inflect.engine()
      
        with open(self.createAbsolutePaths("/classes.pkl"), "rb") as f:
            self.classes = pickle.load(f)
            
        self.ys = YOLOSegmentation(self.createAbsolutePaths("/best.pt"))
        
            
    def createAbsolutePaths(self, relativePath):
        absPath = os.path.dirname(__file__)
        absPath = absPath.replace('\\', '/')
        absPath = absPath + relativePath
        return absPath


    def detect_obj(self, image):
        bboxes, class_ids = self.ys.detect(image)
        
        if (bboxes is None or len(bboxes) == 0):
            return "Cannot detect any cloth in the image."
        detecte_clothes = {}
        
        for i in range(len(bboxes)):
            class_id = class_ids[i]
            detected_object = self.classes[class_id]
            
            cloth_box_image = image[bboxes[i][1]:bboxes[i][3], bboxes[i][0]:bboxes[i][2],:]
            
            plt.imshow(cloth_box_image)
            plt.show()     
        

class YOLOSegmentation:
    def __init__(self, model_path):
        self.model = YOLO(model_path)

    def detect(self, img):
        results = self.model.predict(conf=0.5, source=img.copy(), save=False, save_txt=False)
        result = results[0]
        
        if (result is None or result.boxes is None):
            return None, None

        bboxes = np.array(result.boxes.xyxy.cpu(), dtype="int")
        
        class_ids = np.array(result.boxes.cls.cpu(), dtype="int")
        
        return bboxes, class_ids
    
clothes_detector = ClothesDescriptor()
test_image = cv2.imread("./test2.jpg")
clothes_detector.detect_obj(test_image)