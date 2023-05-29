import sys
from imports import *

sys.path.append("../")


classes = ["Wool", "Denim", "Leather", "Cotton", "Silk"]

WIDTH = 260
HEIGHT = 260


class DataLoader:
    def __init__(self, path: Path):
        self.path = path
        self.first = True

    def load_data(self):
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
                images = []
                # Loop over all files in the subdirectory
                for filename in os.listdir(subdirectory_path):

                    # Read the image file
                    image_path = os.path.join(subdirectory_path, filename)
                    image = cv2.imread(image_path)
                    if image is None or len(image) == 0:
                        continue
                    texture_class = classes.index(directory)

                    image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
                    
                    labels.append(texture_class)
                    images.append(image)
                    
                labels = np.array(labels)
                images = np.array(images)
                x_train_temp, x_val_temp, y_train_temp, y_val_temp = train_test_split(
                    images, labels, test_size=0.15, random_state=42
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

    def crop_center(self, image):
        height, width = image.shape[:2]
        start_row = max(0, int((height - HEIGHT) / 2))
        start_col = max(0, int((width - WIDTH) / 2))
        end_row = min(height, start_row + HEIGHT)
        end_col = min(width, start_col + WIDTH)
        cropped_image = image[start_row:end_row, start_col:end_col]
        return cropped_image
