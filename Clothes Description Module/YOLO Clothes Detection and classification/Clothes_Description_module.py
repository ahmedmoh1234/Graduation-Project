from feature_selection.feature_selection import FeatureSelector
from feature_extraction.feature_extraction import FeatureExtractor
from imports import *

import warnings
warnings.filterwarnings('ignore')

clothes_to_segmentation_classes = {
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
    "watch": [],
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
    "pouchbag": [16]
}
class ClothesDescriptor():
    
    def __init__(self):
        self.p = inflect.engine()
        self.texture_model = load_model("texture_ann.h5")
        self.texture_pca = pickle.load(open("texture_pca.pkl", "rb"))
        self.segmentation_model = pickle.load(open("clothes_segmentation_model.pkl", "rb"))
        self.texture_extracted_features_train_mean = np.load("texture_extracted_features_train_mean.npy")
        self.texture_extracted_features_train_std = np.load("texture_extracted_features_train_std.npy")
        
        self.feature_extractor = FeatureExtractor()
        self.feature_selector = FeatureSelector()
        self.segmentation_extractor = AutoFeatureExtractor.from_pretrained("mattmdjaga/segformer_b2_clothes")
      
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
        
        segmentation_inputs = self.segmentation_extractor(images=image, return_tensors="pt")
        
        segmentation_outputs = self.segmentation_model(**segmentation_inputs)
        logits = segmentation_outputs.logits.cpu()
        upsampled_logits = nn.functional.interpolate(
            logits,
            size=image.shape[:2],
            mode="bilinear",
            align_corners=False,
        )
        
        segmented_image = upsampled_logits.argmax(dim=1)[0]
        
        for i in range(len(bboxes)):
            class_id = class_ids[i]
            detected_object = self.clothes_classes[class_id]
            
            cloth_box_image = image[bboxes[i][1]:bboxes[i][3], bboxes[i][0]:bboxes[i][2],:] # 3D array (width, height, channels)
            
            segmented_cloth = self.select_cloth_pixels(segmented_image, image, detected_object)
                          
            color = self.detect_color(segmented_cloth)
            
            segmentation_inputs = self.segmentation_extractor(images=cloth_box_image, return_tensors="pt")
            
            segmentation_outputs = self.segmentation_model(**segmentation_inputs)
            logits = segmentation_outputs.logits.cpu()
            upsampled_logits = nn.functional.interpolate(
                logits,
                size=cloth_box_image.shape[:2],
                mode="bilinear",
                align_corners=False,
            )
        
            segmented_box = upsampled_logits.argmax(dim=1)[0]
            
            segmented_box_image = self.select_cloth_pixels(segmented_box, cloth_box_image, detected_object)
            
            segmented_box_binary =  np.where(segmented_box_image == 0, 0, 255)[:,:,0].astype(np.uint8)
            plt.imshow(segmented_box_binary)
            plt.show()
            print(f"segmented_box_binary shape: {segmented_box_binary.shape}")
            
            square_min_x, square_min_y, square_max_x, square_max_y = self.find_largest_square(segmented_box_binary)
            cloth_region = cloth_box_image[square_min_y:square_max_y, square_min_x:square_max_x,:] # 3D array (width, height, channels)
            plt.imshow(cloth_region)
            plt.show()

            texture = ""
            
            try:            
                texture = self.detect_texture(cloth_region)
            except:
                texture= ""

            
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
    
    def select_cloth_pixels(self, segmented_image, original_image, cloth_class):
        cloth_class_ids = clothes_to_segmentation_classes[cloth_class]
        cloth_mask = np.isin(segmented_image, cloth_class_ids)
        cloth_pixels = original_image.copy()
        cloth_pixels[~cloth_mask] = 0
        return cloth_pixels
    
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
        temp = unique_colors.copy()
        unique_colors = unique_colors[np.where(np.sum(temp, axis=1) != 0)]
        counts = counts[np.where(np.sum(temp, axis=1) != 0)]
        
        sorted_indices = np.argsort(counts)[::-1]
        unique_colors = unique_colors[sorted_indices]
        counts = counts[sorted_indices]
        dominant_colors = set()
        
        for i in range(len(unique_colors)):
            try:
                color = unique_colors[i]
                named_color = self.rgb_to_name(color)
                dominant_colors.add(named_color)
                if(len(dominant_colors) == 3):
                    break
            except ValueError:
                continue

        dominant_colors_str = ', '.join(dominant_colors)

        return dominant_colors_str

    def rgb_to_name(self,rgb):
        closest_color = None
        min_distance = float('inf')
        
        # Predefined known colors
        known_colors = [
            'red',
            'green',
            'blue',
            'yellow',
            'orange',
            'purple',
            'pink',
            'brown',
            'gray',
            'black'
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

    def color_distance(self,rgb1, rgb2):
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
        results = self.model.predict(conf=0.5, source=img.copy(), save=False, save_txt=False)
        result = results[0]
        
        if (result is None or result.boxes is None):
            return None, None

        bboxes = np.array(result.boxes.xyxy.cpu(), dtype="int")
        
        class_ids = np.array(result.boxes.cls.cpu(), dtype="int")
        
        return bboxes, class_ids
    
clothes_detector = ClothesDescriptor()
test_image = cv2.imread("./test3.jpg")
result = clothes_detector.describe_cloth(test_image)
print(result[0])

