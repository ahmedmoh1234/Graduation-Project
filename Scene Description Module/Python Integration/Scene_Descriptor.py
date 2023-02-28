from ultralytics import YOLO
import pickle


def detect_obj(image):
    model = YOLO("yolov8m.pt")
    results = model.predict(
    task="detect",
    source= image,
    conf=0.5,
    # save=True,
    # save_txt=True,
    # save_crop=True,
    line_thickness=1,
    hide_labels=False,
    hide_conf=False,
    classes=None,
    project = "./predictions",
    name = "test"
    )
    
    # Load the pickle file
    with open("classes.pkl", "rb") as f:
        classes = pickle.load(f)
    
    boxes = ((results[0].boxes)).boxes.numpy()
    results = dict()
    
    for box in boxes:
        # check if the box is already in the dictionary
        if classes[int(box[5])] in results:
            results[classes[int(box[5])]] += 1
        else:
            results[classes[int(box[5])]] = 1
            
    str ="There are "
    for key in results:
        str  +=  f"{results[key]} {key} ,"
    # remove the last comma
    str = str[:-1]
    str+="in the image."
    print(str)
    return str
