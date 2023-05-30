from ultralytics import YOLO
import numpy as np
import inflect
import os
import pickle
import cv2
from matplotlib import pyplot as plt
from imports import *
from feature_selection.feature_selection import FeatureSelector
from feature_extraction.feature_extraction import FeatureExtractor
from preprocessing.clustering_segmentation import ClusteringSegmentation
from preprocessing.region_segmentation import RegionBasedSegmentation
from sklearn.cluster import KMeans
import webcolors
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
        self.clustering_segmentation = ClusteringSegmentation(method='kmeans', n_clusters=2, compactness=30.0, sigma=1.0)
        self.region_based_segmentation = RegionBasedSegmentation(method="region_growing", threshold=0.5)
      
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
        detecte_clothes = {}
        
        for i in range(len(bboxes)):
            class_id = class_ids[i]
            detected_object = self.clothes_classes[class_id]
            
            cloth_box_image = image[bboxes[i][1]:bboxes[i][3], bboxes[i][0]:bboxes[i][2],:] # 3D array (width, height, channels)
            
            # Flatten the ROI to a 2D array
            roi = cloth_box_image # 3D array (width, height, channels)
            rows, cols, _ = roi.shape
            flattened_roi = roi.reshape(rows * cols, -1) # 2D array (rows*cols, channels)
            print(f"flattened_roi shape: {flattened_roi.shape}")
            # Apply k-means clustering
            k = 2  # Number of clusters
            kmeans = KMeans(n_clusters=k, random_state=0)
            labels = kmeans.fit_predict(flattened_roi) # 1D array (rows*cols,)
            print(f"labels shape: {labels.shape}")

            # Calculate the cluster sizes
            _, cluster_sizes = np.unique(labels, return_counts=True)

            # Determine the cloth segment as the cluster with the largest size
            cloth_segment = np.argmax(cluster_sizes) # 0 or 1

            # Generate a mask based on the cloth segment
            mask = np.zeros((rows * cols,), dtype=np.uint8) # 1D array (rows*cols,)
            mask[labels == cloth_segment] = 255
            mask = mask.reshape(rows, cols) # 2D array (rows, cols)

            # Apply the mask on the original ROI
            segmented_cloth = cv2.bitwise_and(roi, roi, mask=mask) # 3D array (width, height, channels)
            
            # Find the largest square region in the segmented cloth
            square_min_x, square_min_y, square_max_x, square_max_y = self.find_largest_square(mask)
            cloth_region = segmented_cloth[square_min_y:square_max_y, square_min_x:square_max_x]
            
            print(f"cloth_region.shape: {cloth_region.shape}")
            # plt.imshow(cloth_region)      
            # plt.show()
            
            color = self.detect_color(segmented_cloth,mask)
            
            # Find the non-zero pixels in the segmented_cloth image
            nonzero_pixels = np.nonzero(segmented_cloth)

            # Get the minimum and maximum row and column indices of the non-zero pixels
            min_row = np.min(nonzero_pixels[0])
            max_row = np.max(nonzero_pixels[0])
            min_col = np.min(nonzero_pixels[1])
            max_col = np.max(nonzero_pixels[1])

            # Extract the non-zero region as a sample
            sample = segmented_cloth[min_row:max_row, min_col:max_col]

            # Pass the sample to the detect_texture function
            texture = self.detect_texture(sample)
            
            print(f"There is a {detected_object} in the image. It is made of {texture}. With color {color}.")
            
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
    

    def detect_color(self, image, mask):
        #  mask is a 2D array and image is a 3D array

        # Get the RGB values of non-zero pixels
        nonzero_image = image[mask != 0]

        # Get the dominant RGB colors in the non-zero pixels
        unique_colors, color_counts = np.unique(nonzero_image, axis=0, return_counts=True)

        # Sort the colors based on their count in descending order
        sorted_colors = sorted(zip(unique_colors, color_counts), key=lambda x: x[1], reverse=True)

        dominant_colors = []
        for color, _ in sorted_colors:
            try:
                closest_name = webcolors.rgb_to_name(color)
                dominant_colors.append(closest_name)
                if(len(dominant_colors) == 3):
                    break
            except ValueError:
                continue

        dominant_colors_str = ', '.join(dominant_colors)

        return dominant_colors_str

    def find_largest_square(self,mask):
        # Find contours in the mask
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Find the contour with the largest area
        largest_contour = max(contours, key=cv2.contourArea)

        # Find the minimum area bounding rectangle
        rect = cv2.minAreaRect(largest_contour)
        box = cv2.boxPoints(rect)
        box = np.int0(box)

        # Find the minimum and maximum coordinates of the bounding box
        min_x = np.min(box[:, 0])
        max_x = np.max(box[:, 0])
        min_y = np.min(box[:, 1])
        max_y = np.max(box[:, 1])

        # Calculate the side length of the square region
        side_length = max(max_x - min_x, max_y - min_y)

        # Adjust the coordinates to form a square region
        center_x = (min_x + max_x) // 2
        center_y = (min_y + max_y) // 2
        half_length = side_length // 2
        square_min_x = center_x - half_length
        square_max_x = center_x + half_length
        square_min_y = center_y - half_length
        square_max_y = center_y + half_length

        return square_min_x, square_min_y, square_max_x, square_max_y

    
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
clothes_detector.describe_cloth(test_image)