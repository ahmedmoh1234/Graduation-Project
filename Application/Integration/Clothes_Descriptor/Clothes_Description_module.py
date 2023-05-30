from ultralytics import YOLO
from tensorflow.keras.models import load_model
import numpy as np
import inflect
import os
import sys
import pickle
import cv2
from matplotlib import pyplot as plt

import pathlib
PATH = pathlib.Path(__file__)

sys.path.insert(0, PATH.resolve())

from feature_selection.feature_selection import FeatureSelector
from feature_extraction.feature_extraction import FeatureExtractor
from sklearn.cluster import KMeans
from webcolors import rgb_to_name

import warnings
warnings.filterwarnings('ignore')


class ClothesDescriptor():
    
    def __init__(self):
        self.p = inflect.engine()
        self.texture_model = load_model("texture_ann.h5")
        self.texture_pca = pickle.load(open("texture_pca.pkl", "rb"))
        self.texture_extracted_features_train_mean = np.load("texture_extracted_features_train_mean.npy")
        self.texture_extracted_features_train_std = np.load("texture_extracted_features_train_std.npy")
        
        self.feature_extractor = FeatureExtractor()
        self.feature_selector = FeatureSelector()
      
        with open(self.createAbsolutePaths("/clothes_classes.pkl"), "rb") as f:
            self.clothes_classes = pickle.load(f)
            
        with open(self.createAbsolutePaths("/texture_classes.pkl"), "rb") as f:
            self.texture_classes = pickle.load(f)
            
        self.ys = YOLOSegmentation(self.createAbsolutePaths("/clothes_detection.pt"))
        
            
    def createAbsolutePaths(self, relativePath):
        absPath = os.path.dirname(__file__)
        absPath = absPath.replace('\\', '/')
        absPath = absPath + relativePath
        return absPath

    def describe_cloth(self, image):
        bboxes, class_ids = self.ys.detect(image)
        
        if (bboxes is None or len(bboxes) == 0):
            return "Cannot detect any cloth in the image."
        detected_clothes = []
        
        for i in range(len(bboxes)):
            class_id = class_ids[i]
            detected_object = self.clothes_classes[class_id]
            
            cloth_box_image = image[bboxes[i][1]:bboxes[i][3], bboxes[i][0]:bboxes[i][2],:] # 3D array (width, height, channels)
            
            roi = cloth_box_image # 3D array (width, height, channels)
            rows, cols, _ = roi.shape
            flattened_roi = roi.reshape(rows * cols, -1) # 2D array (rows*cols, channels)
            
            k = 2  # Number of clusters
            kmeans = KMeans(n_clusters=k, random_state=0)
            labels = kmeans.fit_predict(flattened_roi) # 1D array (rows*cols,)

            _, cluster_sizes = np.unique(labels, return_counts=True)

            cloth_segment = np.argmax(cluster_sizes) # 0 or 1

            mask = np.zeros((rows * cols,), dtype=np.uint8) # 1D array (rows*cols,)
            mask[labels == cloth_segment] = 255
            mask = mask.reshape(rows, cols) # 2D array (rows, cols)
            
            kernel = np.ones((10,10),np.uint8)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

            segmented_cloth = cv2.bitwise_and(roi, roi, mask=mask) # 3D array (width, height, channels)
            
            square_min_x, square_min_y, square_max_x, square_max_y = self.find_largest_square(mask)
            cloth_region = segmented_cloth[square_min_y:square_max_y, square_min_x:square_max_x,:] # 3D array (width, height, channels)
            
            color_val = cloth_region[cloth_region != 0]
            
            if color_val.size != 0:
                 color_val = [color_val[0],color_val[0],color_val[0]]
            else:
                color_val = np.random.randint(0,255,3)
             
            # Replace pixels with 0 mask value
            zero_pixels = np.where(mask[square_min_y:square_max_y, square_min_x:square_max_x] == 0)
            cloth_region[zero_pixels] = color_val
                          
            color = self.detect_color(cloth_region)

            flag = True
            increased_size = 8
            texture = ""
            count_trials = 20
            
            while flag:
                try:            
                    texture = self.detect_texture(cloth_region)
                    flag = False
                except:
                    cloth_region = segmented_cloth[square_min_y - increased_size:square_max_y+increased_size, square_min_x - increased_size:square_max_x + increased_size,:] # 3D array (width, height, channels)   
                    increased_size += 8
                    count_trials -= 1
                    if count_trials == 0:
                        break
            
            detected_clothes.append((detected_object,texture,color))
        
        result = ""
        if len(detected_clothes) ==1:
            result = "There is " + self.p.a(detected_clothes[0][2]) + detected_clothes[0][1] + detected_clothes[0][0] + " in the image."
        
        else:
            result = "There are "
            for i in range(len(detected_clothes)):
                if i == len(detected_clothes) - 1:
                    result += "and " + detected_clothes[i][2] +" " + detected_clothes[i][1] + " " + detected_clothes[i][0] + " in the image."
                else:
                    result += detected_clothes[i][2] + " " + detected_clothes[i][1] + " " + detected_clothes[i][0] + "; "
        print(result)
        return result, detected_clothes
        
    def detect_texture(self,image):
        
        gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        
        image_width = gray_image.shape[1]
        image_height = gray_image.shape[0]
        
        glcm_features = self.feature_extractor.extract_glcm_features([gray_image])[0]
        daisy_features = self.feature_extractor.extract_daisy_features([gray_image],width= min(image_width,260),height= min(image_height,260))[0]
        
        pca_features = self.feature_selector.test_pca(daisy_features,self.texture_pca).flatten()
        pca_features = np.concatenate((pca_features, glcm_features)).reshape(1,-1)
        pca_features = (pca_features - self.texture_extracted_features_train_mean) /self.texture_extracted_features_train_std
        
        model_prediction = self.texture_model.predict(pca_features)
        model_prediction = model_prediction.argmax(axis=1)
        
        predicted_texture = self.texture_classes[int(model_prediction[0])]
        
        return predicted_texture
    

    def detect_color(self, image):

        unique_colors, counts = np.unique(image.reshape(-1, image.shape[-1]), axis=0, return_counts=True)
        
        sorted_indices = np.argsort(counts)[::-1]
        unique_colors = unique_colors[sorted_indices]
        counts = counts[sorted_indices]
        dominant_colors = []
        
        for i in range(len(unique_colors)):
            try:
                color = unique_colors[i]
                named_color = rgb_to_name(tuple(color), spec='css3')
                dominant_colors.append(named_color)
                if(len(dominant_colors) == 3):
                    break
            except ValueError:
                continue

        dominant_colors_str = ', '.join(dominant_colors)

        return dominant_colors_str

    def find_largest_square(self,mask):
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        largest_contour = max(contours, key=cv2.contourArea)

        rect = cv2.minAreaRect(largest_contour)
        box = cv2.boxPoints(rect)
        box = np.int0(box)

        min_x = max(np.min(box[:, 0]),0)
        max_x = None
        
        
        if( np.max(box[:, 0]) < 0):
            max_x = mask.shape[1]
        else: 
            max_x = np.max(box[:, 0])
            
        min_y = max(np.min(box[:, 1]),0)
        
        max_y = None
                
        if( np.max(box[:, 1]) < 0):
            max_y = mask.shape[0]
        else: 
            max_y = np.max(box[:, 1])

        return min_x, min_y, max_x, max_y

    
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
test_image = cv2.imread("./test3.jpg")
clothes_detector.describe_cloth(test_image)