import cv2
import os


#Path to the haar cascade classifier
haarCascadePath = "haarcascade_frontalface_default.xml"

#load haar cascade classifier
faceCascade = cv2.CascadeClassifier(haarCascadePath)

videoCapture = cv2.VideoCapture(0)
while True:
    #Capture frames from camera
    ret, frame = videoCapture.read()

    #Convert to captured image to grayscale
    grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #Detect faces in the image
    faces = faceCascade.detectMultiScale(
        grayscale,                              #image
        scaleFactor=1.1,                        #scale factor (how much the image size is reduced at each image scale)
        minNeighbors=5,                         #minimum number of neighbors to detect a face
        minSize=(30, 30),                       #minimum size of the face
        flags = cv2.CASCADE_SCALE_IMAGE         #flags which specify how to detect the faces
    )

    #Draw a rectangle around the detected faces
    for (x, y, w, h) in faces:
        drawColor = (0, 255, 0)
        cv2.rectangle(frame, (x, y), (x+w, y+h), drawColor, 2)

    #Display the video
    cv2.imshow('Video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#Release the camera and close all windows
videoCapture.release()
cv2.destroyAllWindows()


