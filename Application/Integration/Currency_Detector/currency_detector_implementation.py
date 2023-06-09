from sklearn import preprocessing
#knn classifier
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
import  cv2
import numpy as np
import os
import time
import skimage.io as io
# Path: main.py
import pathlib
PATH = pathlib.Path(__file__).parent
import torch
from PIL import Image
from yolov5 import YOLOv5
from numba import jit, njit

#import train and split
from skimage.feature import graycomatrix, graycoprops
from sklearn.model_selection import train_test_split


def compute_histogram(img,bins):
    #extract the histogram
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hist_img = cv2.calcHist([hsv],[0,1,2],None,bins,[0, 180, 0, 256, 0, 256])
    # print(hist_img.shape)
    # print(hist_img.shape)
    #normalize the histogram
    hist_img = hist_img/np.sum(hist_img)
    hist_img = hist_img.flatten()
    hist_img = hist_img.reshape( 8*8*8,1)
    
    return hist_img
    
def feature_extraction_hist(currency,bins=(8, 8, 8)):
    for i in range(1, 101):
        img = cv2.imread(PATH.resolve()/'datasets/'+currency+'/'+currency+'.'+str(i)+'.jpg')
        hist_img = compute_histogram(img,bins)
        
        if i == 1:
            histogram_set = hist_img
        else:
            histogram_set = np.concatenate((histogram_set, hist_img), axis=1)
    return histogram_set
def compute_glcm(img):
    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Compute the GLCM matrix
    distances = [1, 2, 3]
    angles = [0, np.pi/4, np.pi/2, 3*np.pi/4]
    # greyImg = np.asarray(img.convert('L', colors=8))
    glcm = graycomatrix(gray, distances, angles, levels=256, symmetric=True, normed=True)
    # print("check")
    # Compute texture features from the GLCM matrix
    contrast = graycoprops(glcm, 'contrast').ravel()
    dissimilarity = graycoprops(glcm, 'dissimilarity').ravel()
    homogeneity = graycoprops(glcm, 'homogeneity').ravel()
    energy = graycoprops(glcm, 'energy').ravel()
    correlation = graycoprops(glcm, 'correlation').ravel()

    # Concatenate the texture features into a single feature vector
    feature_vector = np.concatenate((contrast, dissimilarity, homogeneity, energy, correlation))
    # print(feature_vector.shape[0])
    return feature_vector
        


def texture_features(currency):
    
    for i in range(1, 101):
        img = cv2.imread(PATH.resolve()/'datasets/'+currency+'/'+currency+'.'+str(i)+'.jpg')

        feature_vector = compute_glcm(img)
        
        feature_vector = feature_vector.reshape(60,1)
        #append the currency name at the start of the feature vector0
        feature_vector = np.insert(feature_vector, 0, currency, axis=0)
        # print(feature_vector)
        
        if i == 1:
            
            all_features = feature_vector
        else:
            # print(all_features.shape)
            # print(feature_vector.shape)
            all_features = np.concatenate((all_features, feature_vector), axis=1)
    
    #normalize the feature vector
    # all_features = all_features/np.sum(all_features)
    return all_features

def prepare_image(testImg):
    
    test_tf = compute_glcm(testImg)
    test_hist = compute_histogram(testImg, (8,8,8))
    test_tf = test_tf.reshape(60,1)
    test_hist = test_hist.reshape(8*8*8,1)
    test = np.concatenate((test_tf,test_hist), axis=0)
    test = test.flatten()
    test = test.reshape(572,1)
    #normalize the test image
    test = test/np.linalg.norm(test)
    print(test.shape)
    return test
## Ones label
# read csv file



def calculateDistance(x1, x2):
    # Euclidean distance
    distance = np.linalg.norm(x1-x2)
    return distance
def KNN(test_points, training_features, labels, k):
    # INPUTS:   test_points: (M_test, N)
    #           training_features: (M, N)
    #           k: the number of nearest neighbours. 
    
    # OUTPUTS:  classification: currency of the test point
    #                           

    distances = [calculateDistance(test_points, p) for p in training_features]

    # distances = np.sqrt(((test_points[:, np.newaxis, :] - training_features) ** 2).sum(axis=2))
    
    k_nearest = np.argpartition(distances, k)[:k]
    
    ones_votes = 0
    fives_votes = 0
    tens_votes = 0
    twenties_votes = 0
    fifties_votes = 0
    hundreds_votes = 0
    twohundreds_votes = 0
    

    for i in k_nearest:
        #check the label of the nearest currency
        if labels[i] == 1:
            ones_votes += 1
        elif labels[i] == 5:
            fives_votes += 1
        elif labels[i] == 10:
            tens_votes += 1
        elif labels[i] == 20:
            twenties_votes += 1
        elif labels[i] == 50:
            fifties_votes += 1
        elif labels[i] == 100:
            hundreds_votes += 1
        elif labels[i] == 200:
            twohundreds_votes += 1
            
    #find the label with the most votes and return the name and count as dict
    votes = {'1': ones_votes, '5': fives_votes, '10': tens_votes, '20': twenties_votes, '50': fifties_votes, '100': hundreds_votes, '200': twohundreds_votes}
    classification = max(votes, key=votes.get)
    
    
    

    return classification

def currency_detect(testImg):
    datasetcsv = np.loadtxt(PATH.resolve()/"dataset.csv", delimiter=",")
    print(datasetcsv.shape)
    #normalize the dataset
    #separate the labels
    # y_dataset = datasetcsv[:, 573:580]
    y_expected = datasetcsv[:, 0]
    dataset = datasetcsv[:, 1:573]
    print(dataset.shape)
    # print(y_dataset.shape)
    print(y_expected.shape)

    #normalize the dataset
    dataset = preprocessing.normalize(dataset, norm='l2')
    print(dataset.shape)


    # #duplicate y_expected
    for i in range(0, 4):
        y_expected = np.concatenate((y_expected, y_expected), axis=0)
        dataset = np.concatenate((dataset, dataset), axis=0)
        # y_dataset = np.concatenate((y_dataset, y_dataset), axis=0)
    
    print(y_expected.shape)
    print(dataset.shape)
    # print(y_dataset.shape)
    print(testImg.shape)
    test = prepare_image(testImg)       
    
    x_train, x_test, y_train, y_test = train_test_split(dataset, y_expected, test_size=0.2, random_state=42)
    #use knn model

    # print("Training knn model...")
    knn = KNeighborsClassifier(n_neighbors=7)


    y_train = y_train.flatten()
    knn.fit(x_train, y_train)
    # print("Training complete!")
    # print("Making predictions...")

    prediction_knn = knn.predict(test.T)
    # print(prediction_knn)

    # predictions_3 = KNN(test.T, x_train, y_train, 3)
    # predictions_5 = KNN(test.T, x_train, y_train, 5)

    # print("predictions_3",predictions_3)
    # print("predictions_5",predictions_5)

    return str(int(prediction_knn[0]))
# imgpath20 = PATH.resolve()/'datasets/20/20.2.jpg'
# imgpath = PATH.resolve()/'20LE_1.jpg'

# testImg = cv2.imread(str(imgpath))
# print(testImg.shape)
# print(currency_detect(testImg))

def boundedBox(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Example: Gaussian blur and Canny edge detection
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    def is_egyptian_bill(contour):
        # Calculate properties like aspect ratio and area
        x, y, w, h = cv2.boundingRect(contour)
        aspect_ratio = float(w) / h
        area = cv2.contourArea(contour)

        # Compare the calculated properties to the expected values for a bill
        if min_aspect_ratio <= aspect_ratio <= max_aspect_ratio and min_area <= area <= max_area:
            return True

        return False

    # Set the expected aspect ratio and area values for an Egyptian bill
    min_aspect_ratio, max_aspect_ratio = 1.5, 2.5  # Adjust these values as needed
    min_area, max_area = 1000, 100000  # Adjust these values as needed

    # Filter contours based on the custom function
    filtered_contours = [cnt for cnt in contours if is_egyptian_bill(cnt)]
    
    for cnt in filtered_contours:
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.imshow("Egyptian Bill Detection", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    for cnt in filtered_contours:
        x, y, w, h = cv2.boundingRect(cnt)
        egyptian_bill = image[y:y+h, x:x+w]
    # Save or process the bill as needed

    cv2.imshow("Egyptian Bill ", egyptian_bill)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return egyptian_bill

# boundedBox(testImg)

# import cv2
# import numpy as np


