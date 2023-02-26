import pickle
import cv2

def describe_clothes(image):
    
    # Load the saved model from a .pkl file
    with open('clothing_detector.pkl', 'rb') as f:
        model = pickle.load(f)
        
    classes = ['T-Shirt' 'Shoes' 'Shorts' 'Shirt' 'Pants' 'Skirt' 'Top' 'Outwear'
    'Dress' 'Body' 'Longsleeve' 'Undershirt' 'Hat' 'Polo' 'Blouse' 'Hoodie'
    'Skip' 'Blazer']
    
    IMAGE_HEIGHT =  128
    IMAGE_WIDTH = 128
    image = cv2.resize(image, (IMAGE_HEIGHT, IMAGE_WIDTH))

    predicted = model.predict(image)
    result = classes[predicted]
    return "The clothes is a " + result + "."