from ultralytics import YOLO
from tensorflow.keras.models import load_model
import numpy as np
import inflect
import os
import sys
import pickle
import torch
import cv2
from matplotlib import pyplot as plt
from mrcnn.config import Config
from mrcnn.model import MaskRCNN
import warnings
from feature_selection.feature_selection import FeatureSelector
from feature_extraction.feature_extraction import FeatureExtractor
from sklearn.cluster import KMeans
from webcolors import rgb_to_name
from imports import *

warnings.filterwarnings("ignore")

import pathlib

PATH = pathlib.Path(__file__)

PARENT = PATH.parent

sys.path.append(str(PATH.parent))

import warnings

warnings.filterwarnings("ignore")


class TestConfig(Config):
    NAME = "test"
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1

    if torch.cuda.is_available():
        GPU_COUNT = torch.cuda.device_count()

    NUM_CLASSES = 1 + 13


class ClothesDescriptor:
    def __init__(self):
        self.p = inflect.engine()
        self.texture_model = load_model(PARENT.resolve() / "texture_ann.h5")
        self.texture_pca = pickle.load(open(PARENT.resolve() / "texture_pca.pkl", "rb"))
        self.texture_extracted_features_train_mean = np.load(
            PARENT.resolve() / "texture_extracted_features_train_mean.npy"
        )
        self.texture_extracted_features_train_std = np.load(
            PARENT.resolve() / "texture_extracted_features_train_std.npy"
        )

        self.feature_extractor = FeatureExtractor()
        self.feature_selector = FeatureSelector()

        with open(PARENT.resolve() / "clothes_classes.pkl", "rb") as f:
            self.ecommerce_clothes_classes = pickle.load(f)

        with open(PARENT.resolve() / "texture_classes.pkl", "rb") as f:
            self.texture_classes = pickle.load(f)

        self.ys = YOLOSegmentation(PARENT.resolve() / "clothes_detection.pt")
        self.segmentation_model = pickle.load(
            open("clothes_segmentation_model.pkl", "rb")
        )
        self.segmentation_extractor = AutoFeatureExtractor.from_pretrained(
            "mattmdjaga/segformer_b2_clothes"
        )

        self.rcnn = MaskRCNN(mode="inference", model_dir="./", config=TestConfig())
        self.rcnn.load_weights("./mask_rcnn_deepfashion2_0100.h5", by_name=True)

        self.deepfashion_clothes_classes = [
            "T_shirt",
            "shirt",
            "short sleeved jacket",
            "long sleeved jacket",
            "jacket",
            "sling",
            "shorts",
            "trousers",
            "skirt",
            "short sleeved dress",
            "long sleeved dress",
            "vest dress",
            "sling dress",
        ]

        self.deepfashion_clothes_to_segmentation_classes = {
            "T_shirt": [4],
            "shirt": [4],
            "short sleeved jacket": [4],
            "long sleeved jacket": [4],
            "jacket": [4],
            "sling": [8],
            "shorts": [],
            "trousers": [6],
            "skirt": [5],
            "short sleeved dress": [8],
            "long sleeved dress": [8],
            "vest dress": [8],
            "sling dress": [8],
        }
        self.ecommerce_upper_ids = [1, 2, 5, 7]
        self.ecommerce_bottom_ids = [0, 18]

        self.deepfashion_upper_ids = [0, 1, 2, 3, 4, 5]
        self.deepfashion_bottom_ids = [7]

        self.detected_upper = False
        self.detected_lower = False

        self.ecommerce_clothes_to_segmentation_classes = {
            "trousers": [6],
            "coat": [4],
            "jacket": [4],
            "belt": [8],
            "necklace": [],
            "vest": [4],
            "ring": [],
            "shirt": [4],
            "hat": [1],
            "bracelet": [],
            "tie": [],
            "bag": [16],
            "watche": [],
            "scarf": [17],
            "boot": [9, 10],
            "sportshoes": [9, 10],
            "sunglasses": [3],
            "earrings": [],
            "skirt": [5],
            "dress": [7],
            "socks and tight": [],
            "shoes": [9, 10],
            "underwear": [],
            "backpack": [16],
            "short": [6],
            "night morning": [],
            "gloves and mitten": [],
            "wallet and purse": [],
            "cufflinks": [],
            "swimwear": [],
            "makeup": [],
            "suitcase": [16],
            "jumpsuit": [7],
            "suspenders": [],
            "pouchbag": [16],
        }

    def describe_cloth(self, image):
        bboxes, class_ids = self.ys.detect(image)
        
        detected_clothes = []

        segmentation_inputs = self.segmentation_extractor(
            images=image, return_tensors="pt"
        )

        segmentation_outputs = self.segmentation_model(**segmentation_inputs)
        logits = segmentation_outputs.logits.cpu()
        upsampled_logits = nn.functional.interpolate(
            logits,
            size=image.shape[:2],
            mode="bilinear",
            align_corners=False,
        )

        segmented_image = upsampled_logits.argmax(dim=1)[0]
        plt.imshow(segmented_image)
        plt.show()
        if not (bboxes is None):
            for i in range(len(bboxes)):
                class_id = class_ids[i]
                detected_object = self.ecommerce_clothes_classes[class_id]

                box_cloth_image = image[
                    bboxes[i][1] : bboxes[i][3], bboxes[i][0] : bboxes[i][2]
                ]
                segmented_cloth = self.select_cloth_pixels(
                    segmented_image, image, detected_object, 0
                )
                plt.imshow(segmented_cloth)
                plt.show()

                if self.ecommerce_clothes_to_segmentation_classes[detected_object] == []:
                    detected_clothes.append((detected_object, "", ""))
                    continue

                if self.ecommerce_upper_ids.__contains__(class_id):
                    self.detected_upper = True

                elif self.ecommerce_bottom_ids.__contains__(class_id):
                    self.detected_lower = True

                color = self.detect_color(segmented_cloth)

                cloth_region = None
                try:
                    cloth_region = self.get_nonzero_rectangle(segmented_cloth)
                    if(cloth_region.shape[0] <260 or cloth_region.shape[1] <260):
                        cloth_region = box_cloth_image
                except:
                    cloth_region = box_cloth_image

                plt.imshow(cloth_region)
                plt.show()
                texture = ""

                try:
                    texture = self.detect_texture(cloth_region)
                except:
                    texture = ""

                detected_clothes.append((detected_object, texture, color))
        try:
            if not self.detected_upper or not self.detected_lower:
                results = self.rcnn.detect([image], verbose=1)
                r = results[0]
                bboxes = r["rois"]
                class_ids = r["class_ids"]
                for i, class_id in enumerate(class_ids):
                    detected_object = self.deepfashion_clothes_classes[class_id]
                    box_cloth_image = image[
                        bboxes[i][0] : bboxes[i][2], bboxes[i][1] : bboxes[i][3]
                    ]

                    if not self.detected_upper and self.deepfashion_upper_ids.__contains__(class_id):
                        self.detected_upper = True
                    elif not self.detected_lower and self.deepfashion_bottom_ids.__contains__(class_id):
                        self.detected_lower = True
                    else:
                        continue

                    segmented_cloth = self.select_cloth_pixels(
                        segmented_image, image, detected_object, 1
                    )
                    plt.imshow(segmented_cloth)
                    plt.show()
                    color = self.detect_color(segmented_cloth)

                    cloth_region = None
                    try:
                        cloth_region = self.get_nonzero_rectangle(segmented_cloth)
                    except:
                        cloth_region = box_cloth_image

                    plt.imshow(cloth_region)
                    plt.show()
                    texture = ""
                    
                    try:
                        texture = self.detect_texture(cloth_region)
                    except:
                        texture = ""

                    detected_clothes.append((detected_object, texture, color))
        except:
            pass
        
        if len(detected_clothes) == 0:
            return "Cannot detect any cloth in the image."
             
        result = ""
        if len(detected_clothes) == 1:
            result = (
                "There is "
                + self.p.a(detected_clothes[0][2])
                + detected_clothes[0][1]
                + detected_clothes[0][0]
                + " in the image."
            )

        else:
            result = "There are "
            for i in range(len(detected_clothes)):
                if i == len(detected_clothes) - 1:
                    result += (
                        "and "
                        + detected_clothes[i][2]
                        + " "
                        + detected_clothes[i][1]
                        + " "
                        + detected_clothes[i][0]
                        + " in the image."
                    )
                else:
                    result += (
                        detected_clothes[i][2]
                        + " "
                        + detected_clothes[i][1]
                        + " "
                        + detected_clothes[i][0]
                        + "; "
                    )
        print(result)
        return result, detected_clothes

    def select_cloth_pixels(
        self, segmented_image, original_image, cloth_class, dataset_type
    ):
        cloth_class_ids = []
        if dataset_type == 0:
            cloth_class_ids = self.ecommerce_clothes_to_segmentation_classes[
                cloth_class
            ]
        else:
            cloth_class_ids = self.deepfashion_clothes_to_segmentation_classes[
                cloth_class
            ]
        cloth_mask = np.isin(segmented_image, cloth_class_ids)
        cloth_pixels = original_image.copy()
        cloth_pixels[~cloth_mask] = 0
        return cloth_pixels
    
    def get_nonzero_rectangle(self, image):
        
        # Convert image to binary format
        gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

        # Find contours in the binary_cloth image
        contours, _ = cv2.findContours(gray_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        largest_contour = max(contours, key=cv2.contourArea)

        rect = cv2.minAreaRect(largest_contour)
        box = cv2.boxPoints(rect)
        box = np.int0(box)

        min_x = max(np.min(box[:, 0]), 0)
        max_x = min(np.max(box[:, 0]), image.shape[1])

        min_y = max(np.min(box[:, 1]), 0)
        max_y = min(np.max(box[:, 1]), image.shape[0])
        
        cloth_region = image[min_y:max_y, min_x:max_x]
        return cloth_region
    
    def detect_texture(self, image):
        gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

        image_width = gray_image.shape[1]
        image_height = gray_image.shape[0]

        glcm_features = self.feature_extractor.extract_glcm_features([gray_image])[0]
        daisy_features = self.feature_extractor.extract_daisy_features(
            [gray_image], width=min(image_width, 260), height=min(image_height, 260)
        )[0]

        pca_features = self.feature_selector.test_pca(
            daisy_features, self.texture_pca
        ).flatten()
        pca_features = np.concatenate((pca_features, glcm_features)).reshape(1, -1)
        pca_features = (
            pca_features - self.texture_extracted_features_train_mean
        ) / self.texture_extracted_features_train_std

        model_prediction = self.texture_model.predict(pca_features)
        model_prediction = model_prediction.argmax(axis=1)

        predicted_texture = self.texture_classes[int(model_prediction[0])]

        return predicted_texture

    def detect_color(self, image):
        unique_colors, counts = np.unique(
            image.reshape(-1, image.shape[-1]), axis=0, return_counts=True
        )
        temp = unique_colors.copy()
        unique_colors = unique_colors[np.where(np.sum(temp, axis=1) != 0)]
        counts = counts[np.where(np.sum(temp, axis=1) != 0)]

        sorted_indices = np.argsort(counts)[::-1]
        unique_colors = unique_colors[sorted_indices]
        counts = counts[sorted_indices]
        # unordered set of dominant colors
        dominant_colors = dict()

        # for i in range(len(unique_colors)):
        # try:
        color = unique_colors[0]

        named_color = self.rgb_to_name(color)
        dominant_colors[named_color] = None
        # if(len(dominant_colors) == 3):
        #     break
        # except ValueError:

        dominant_colors = list(dominant_colors.keys())
        dominant_colors_str = ", ".join(dominant_colors)

        return dominant_colors_str

    def rgb_to_name(self, rgb):
        closest_color = None
        min_distance = float("inf")

        # Predefined known colors
        known_colors = [
            "red",
            "green",
            "blue",
            "yellow",
            "orange",
            "purple",
            "pink",
            "brown",
            "gray",
            "black",
            "white",
            "cyan",
            "magenta",
            "olive",
            "teal",
            "navy",
            "salmon",
            "gold",
            "lavender",
            "turquoise",
            "beige"
        ]

        for color_name in known_colors:
            try:
                color_rgb = webcolors.name_to_rgb(color_name)
                distance = self.color_distance(rgb, color_rgb)

                if distance < min_distance:
                    min_distance = distance
                    closest_color = color_name
            except ValueError:
                continue

        return closest_color

    def color_distance(self, rgb1, rgb2):
        r1, g1, b1 = rgb1
        r2, g2, b2 = rgb2

        distance = ((r2 - r1) ** 2) + ((g2 - g1) ** 2) + ((b2 - b1) ** 2)
        return distance

    def find_largest_square(self, mask):
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        largest_contour = max(contours, key=cv2.contourArea)

        rect = cv2.minAreaRect(largest_contour)
        box = cv2.boxPoints(rect)
        box = np.int0(box)

        min_x = max(np.min(box[:, 0]), 0)
        max_x = min(np.max(box[:, 0]), mask.shape[1])

        min_y = max(np.min(box[:, 1]), 0)
        max_y = min(np.max(box[:, 1]), mask.shape[0])

        return min_x, min_y, max_x, max_y


class YOLOSegmentation:
    def __init__(self, model_path):
        self.model = YOLO(model_path)

    def detect(self, img):
        results = self.model.predict(
            conf=0.5, source=img.copy(), save=False, save_txt=False
        )
        result = results[0]

        if result is None or result.boxes is None:
            return None, None

        bboxes = np.array(result.boxes.xyxy.cpu(), dtype="int")

        class_ids = np.array(result.boxes.cls.cpu(), dtype="int")

        return bboxes, class_ids


clothes_detector = ClothesDescriptor()
test_image = cv2.imread("./test6.jpg")
result = clothes_detector.describe_cloth(test_image)