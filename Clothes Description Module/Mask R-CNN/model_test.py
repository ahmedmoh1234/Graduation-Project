from mrcnn.config import Config
from mrcnn.model import MaskRCNN

import skimage 
import numpy as np
import warnings
import torch
import cv2

warnings.filterwarnings("ignore")

class_names = ['T_shirt', 'shirt', 'short sleeved jacket', 'long sleeved jacket', 'jacket', 'sling', 
               'shorts', 'trousers', 'skirt', 'short sleeved dress', 'long sleeved dress',
               'vest dress', 'sling dress']

accepted_class_ids = [ 0, 1, 2,3,4,6,7] 

class TestConfig(Config):
     NAME = "test"
     GPU_COUNT = 1
     IMAGES_PER_GPU = 1
     
     if torch.cuda.is_available():
          GPU_COUNT = torch.cuda.device_count()
          
     NUM_CLASSES = 1 + 13

rcnn = MaskRCNN(mode='inference', model_dir='./', config=TestConfig())
rcnn.load_weights('./mask_rcnn_deepfashion2_0100.h5', by_name=True)
# img = skimage.io.imread('./test6.jpg')
img = cv2.imread('./test6.jpg')
results = rcnn.detect([img], verbose=1)
r = results[0]
# visualize.display_instances(img, r['rois'], r['masks'], r['class_ids'], class_names, r['scores'])

# Save images of all the masks for different class_ids
masks = r['masks']
class_ids = r['class_ids']

for i, class_id in enumerate(class_ids):
    detected_class = class_names[class_id]
    
    if(accepted_class_ids.count(class_id) == 0):
        continue
   
    mask = masks[:, :, i].astype(np.uint8)
    mask = np.array(mask)
    masked_image = img * np.expand_dims(mask, axis=2)
    name = f"./detected_{detected_class}.jpg"
    skimage.io.imsave(name, masked_image)