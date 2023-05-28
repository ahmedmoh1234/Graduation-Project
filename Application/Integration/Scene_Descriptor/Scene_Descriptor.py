from ultralytics import YOLO
import pickle
import sys
import os
from ultralytics import YOLO
import numpy as np
import cv2
import torch
import urllib.request
import matplotlib.pyplot as plt
import pickle
import inflect
sys.path.insert(0, os.path.dirname(__file__))

class SceneDescriptor():
    def __init__(self, model_path):
            
        self.p = inflect.engine()

        # Load the pickle files
        with open(self.createAbsolutePaths("/classes.pkl"), "rb") as f:
            self.classes = pickle.load(f)
        
        with open(self.createAbsolutePaths("/objects_real_width.pkl"), "rb") as f:
            self.objects_real_width = pickle.load(f)
        

        # Instantiate YOLOSegmentation object
        self.ys = YOLOSegmentation(self.createAbsolutePaths("/yolov8m-seg.pt"))

        model_type = "DPT_Large"     # MiDaS v3 - Large     (highest accuracy, slowest inference speed)
        #model_type = "DPT_Hybrid"   # MiDaS v3 - Hybrid    (medium accuracy, medium inference speed)
        #model_type = "MiDaS_small"  # MiDaS v2.1 - Small   (lowest accuracy, highest inference speed)

        self.midas = torch.hub.load("intel-isl/MiDaS", model_type)
        
        self.device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
        self.midas.to(self.device)

        midas_transforms = torch.hub.load("intel-isl/MiDaS", "transforms")

        if model_type == "DPT_Large" or model_type == "DPT_Hybrid":
            self.transform = midas_transforms.dpt_transform
        else:
            self.transform = midas_transforms.small_transform

    def createAbsolutePaths(self, relativePath):
        absPath = os.path.dirname(__file__)
        absPath = absPath.replace('\\', '/')
        absPath = absPath + relativePath
        return absPath

    def estimate_depth(self, image):  
        input_batch = self.transform(image).to(self.device)

        with torch.no_grad():
            prediction = self.midas(input_batch)

            prediction = torch.nn.functional.interpolate(
                prediction.unsqueeze(1),
                size=image.shape[:2],
                mode="bicubic",
                align_corners=False,
            ).squeeze()

        # Call the detect function
        bboxes, class_ids, seg, scores = self.ys.detect(image)

        # Check for None
        if (seg == None or len(seg) == 0):
            return "There are no objects in the image"

        gray_heat_map = prediction.cpu().numpy()
        gray_heat_map = gray_heat_map.astype(np.uint8)


        close_objects = dict()
        far_objects = dict()
        # Iterate over each segment in seg
        for i in range(len(seg)):
            # Create a blank mask image of the same size as the original image
            mask = np.zeros_like(gray_heat_map[:,:])
            class_id = class_ids[i]
            detected_object = self.classes[class_id]

            # Convert the segment to a NumPy array and round the coordinates to integers
            segment = np.array(seg[i], dtype=np.int32)

            # Get the bounding rectangle of the segment
            x, y, w, h = cv2.boundingRect(segment)
            
            # Print the width and height of the bounding rectangle
            print('===============================')
            print(f"Object: {detected_object}")
            print("Width:", w)
            print("Height:", h)
            
            # Draw the contour on the mask image
            cv2.drawContours(mask, [segment], -1, (255), thickness=cv2.FILLED)
            segmented_image = cv2.bitwise_and(gray_heat_map, gray_heat_map, mask=mask)

            gray_segmented_image = segmented_image / 255.0

            # gray_segmented_image = cv2.cvtColor(segmented_image,cv2.COLOR_BGR2GRAY) / 255.0

            depth_value = np.max(gray_segmented_image) #depth_value is the depth value obtained from the depth map

            object_pixel_width = max(w,h) # object_pixel_width is the width of the object's bounding box in pixels.

            object_width = self.objects_real_width[detected_object]

            # distance_to_object = (object_width * focal_length) / (object_pixel_width * depth_value)
            # print(f"distance_to_object = ({object_width} * {focal_length}) / ({object_pixel_width} * {depth_value})")

            X = (object_width) / (object_pixel_width * depth_value)
            distance_to_object = (67.4  * X) + 19.4

            if (distance_to_object < 100):
                if detected_object in close_objects:
                    close_objects[detected_object] += 1
                else:
                    close_objects[detected_object] = 1
            else:
                if detected_object in far_objects:
                    far_objects[detected_object] += 1
                else:
                    far_objects[detected_object] = 1


        str_result = ''
        if (len(close_objects) != 0):
            if (len(close_objects) == 1):
                class_name = list(close_objects.keys())[0]
                count = close_objects[class_name]
                if (count == 1):
                    str_result = f"There is {count} {class_name}"
                else:
                    str_result = f"There are {count} {self.p.plural(class_name)}"
            else:
                str_result = 'There are'
                for class_name, count in close_objects.items():
                    if (count == 1):
                        str_result += f" {count} {class_name},"
                    else:
                        str_result += f" {count} {self.p.plural(class_name)},"
            
                # Remove the last letter
                str_result = str_result[:-1]
            str_result += ' closer than 1 meter from you.'


        if (len(far_objects) != 0):
            if (len(far_objects) == 1):
                class_name = list(far_objects.keys())[0]
                count = far_objects[class_name]
                if (count == 1):
                    str_result += f"There is {count} {class_name}"
                else:
                    str_result += f"There are {count} {self.p.plural(class_name)}"
            else:
                str_result += 'There are'
                for class_name, count in far_objects.items():
                    if (count == 1):
                        str_result += f" {count} {class_name},"
                    else:
                        str_result += f" {count} {self.p.plural(class_name)},"
            
                # Remove the last letter
                str_result = str_result[:-1]
            str_result += ' further than 1 meter from you.'

        print(str_result)
        return str_result
        

            








class YOLOSegmentation:
    def __init__(self, model_path):
        self.model = YOLO(model_path)

    def detect(self, img):
        # Get image shape
        height, width, channels = img.shape
        results = self.model.predict(conf=0.5, source=img.copy(), save=False, save_txt=False)
        result = results[0]
        segmentation_countours_indx = []
        if (result is None or result.masks is None or result.boxes is None):
            return None, None, None, None
        
        for seg in result.masks.segments:
            # contours
            seg[:, 0] *= width
            seg[:, 1] *= height
            segment = np.array(seg, dtype=np.int32)
            segmentation_countours_indx.append(segment)

        bboxes = np.array(result.boxes.xyxy.cpu(), dtype="int")
        # Get the class ids
        class_ids = np.array(result.boxes.cls.cpu(), dtype="int")

        # Get scores
        scores = np.array(result.boxes.conf.cpu(), dtype="float").round(2)
        
        return bboxes, class_ids, segmentation_countours_indx, scores