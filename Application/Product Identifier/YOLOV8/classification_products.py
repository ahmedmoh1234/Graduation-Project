from ultralytics import YOLO

class BrandRecognition:
    model = None

    def __init__(self, model_path):
        self.model = YOLO(model_path)

    def predict(self, image_path)-> str:

        if self.model is None:
            return "Model not loaded"
        
        results = self.model.predict(image_path)

        if len(results[0].boxes) == 0:
            return "No logo detected"
        
        box = results[0].boxes[0]

        names_dict = results[0].names

        return names_dict[box.cls.item()]


# if __name__ == "__main__":
#     yolo = BrandRecognition('bestNew.pt')

#     for img in os.listdir('test_images'):
#         print(yolo.predict('test_images/'+img))
    


    
    

