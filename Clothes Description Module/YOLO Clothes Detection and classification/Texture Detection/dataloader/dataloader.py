import sys

sys.path.append("../")
from feature_extraction.feature_extraction import FeatureExtractor
from feature_selection.feature_selection import FeatureSelector


from imports import *

classes = ["Wool", "Denim", "Leather", "Cotton", "Silk"]

WIDTH = 260
HEIGHT = 260


class DataLoader:
    def __init__(self, path: Path):
        self.path = path
        self.feature_extractor = FeatureExtractor()
        self.feature_selector = FeatureSelector()
        self.first = True

    def load_data(self):
        labels = []
        x_train = []
        y_train = []
        x_test = []
        y_test = []
        x_val = []
        y_val = []
        # loop over all the directories in the path
        for root, dirs, _ in os.walk(self.path):
            for directory in dirs:
                # Get the path of the current subdirectory
                subdirectory_path = os.path.join(root, directory)
                labels = []
                glcm_features = []
                daisy_features = []
                # Loop over all files in the subdirectory
                for filename in os.listdir(subdirectory_path):

                    # Read the image file
                    image_path = os.path.join(subdirectory_path, filename)
                    image = cv2.imread(image_path)
                    if image is None or len(image) == 0:
                        continue
                    texture_class = classes.index(directory)

                    image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

                    glcm_feat = self.feature_extractor.extract_glcm_features(
                        [image]
                    )[0]
                    image = self.crop_center(image, min(WIDTH,image.shape[1]),min(HEIGHT,image.shape[0]))

                    daisy_feat = self.feature_selector.extract_daisy_features(
                        [image]
                    )[0]
                    glcm_features.append(np.array(glcm_feat))
                    daisy_features.append(np.array(daisy_feat))

                    labels.append(texture_class)
                    
                
                glcm_features = np.array(glcm_features)
                daisy_features = np.array(daisy_features)
                
                print(f"daisy_features shape: {daisy_features.shape}")
                pca_features = None
                if(self.first):
                    pca_features = self.feature_selector.extract_pca_features(
                        daisy_features, load=False, num_pca_components= 50
                    )
                    self.first = False
                else:
                    pca_features = self.feature_selector.extract_pca_features(
                        daisy_features, load=True, num_pca_components= 50
                    )

                images_features = np.concatenate((glcm_features, pca_features), axis=1)

                x_train_temp, x_val_temp, y_train_temp, y_val_temp = train_test_split(
                    images_features, labels, test_size=0.15, random_state=42
                )
                x_train_temp, x_test_temp, y_train_temp, y_test_temp = train_test_split(
                    x_train_temp, y_train_temp, test_size=0.15 / 0.85, random_state=42
                )
                x_train.extend(x_train_temp)
                y_train.extend(y_train_temp)
                x_test.extend(x_test_temp)
                y_test.extend(y_test_temp)
                x_val.extend(x_val_temp)
                y_val.extend(y_val_temp)

        x_train = np.array(x_train)
        y_train = np.array(y_train)
        x_test = np.array(x_test)
        y_test = np.array(y_test)
        x_val = np.array(x_val)
        y_val = np.array(y_val)

        # shuffle the training data
        indices = np.arange(x_train.shape[0])
        np.random.shuffle(indices)
        x_train = x_train[indices]
        y_train = y_train[indices]

        # shuffle the validation data
        indices = np.arange(x_val.shape[0])
        np.random.shuffle(indices)
        x_val = x_val[indices]
        y_val = y_val[indices]

        return x_train, y_train, x_test, y_test, x_val, y_val

    def crop_center(self, image, crop_width, crop_height):
        height, width = image.shape[:2]
        start_row = max(0, int((height - crop_height) / 2))
        start_col = max(0, int((width - crop_width) / 2))
        end_row = min(height, start_row + crop_height)
        end_col = min(width, start_col + crop_width)
        cropped_image = image[start_row:end_row, start_col:end_col]
        return cropped_image
