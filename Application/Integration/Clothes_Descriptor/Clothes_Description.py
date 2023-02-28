import cv2
import io
import numpy as np
import os
import random
import pickle
import tensorflow as tf
import keras 
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.models import Model
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

def createAbsolutePaths(relativePath):
    absPath = os.path.dirname(__file__)
    absPath = absPath.replace('\\', '/')
    absPath = absPath + relativePath
    return absPath

def describe_clothes(image):
    IMAGE_HEIGHT =  128
    IMAGE_WIDTH = 128
    
    # classes = ['T-Shirt', 'Shoes', 'Shorts', 'Shirt', 'Pants', 'Skirt', 'Top', 'Outwear',
    # 'Dress', 'Body' ,'Longsleeve' ,'Undershirt' ,'Hat', 'Polo', 'Blouse', 'Hoodie',
    # 'Skip', 'Blazer']
    
    # # save the classes to a pickle file
    # with open("classes.pkl", "wb") as f:
    #     pickle.dump(classes, f)
        
    # Load the pickle file
    with open(createAbsolutePaths("/classes.pkl"), "rb") as f:
        classes = pickle.load(f)
    
    # Load the saved model from a .pkl file
    # with open('clothing_detector.pkl', 'rb') as f:
    #     model = pickle.load(f)
    resnet_model = ResNet50(weights='imagenet', include_top=False, input_shape=(IMAGE_HEIGHT, IMAGE_WIDTH, 3))

    # Freeze the pre-trained layers to avoid changing their weights during training
    for layer in resnet_model.layers:
        layer.trainable = True

    # Add a new fully connected layer for the specific classification task
    x = Flatten()(resnet_model.output)
    x = Dense(512, activation='relu', input_shape = (IMAGE_HEIGHT, IMAGE_WIDTH, 3),kernel_regularizer=tf.keras.regularizers.l2(0.5))(x)
    x = tf.keras.layers.Dropout(0.5)(x)
    x = Dense(len(classes), activation='linear', input_shape = (IMAGE_HEIGHT, IMAGE_WIDTH, 3),kernel_regularizer=tf.keras.regularizers.l2(0.5))(x)

    # Create a new model by combining the pre-trained ResNet50 model with the new fully connected layers
    model = Model(inputs=resnet_model.input, outputs=x)

    # Compile the model
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),
                loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                metrics=['accuracy'])
    
    model.load_weights(createAbsolutePaths('/clothes_description.h5'))        

    image = cv2.resize(image, (IMAGE_HEIGHT, IMAGE_WIDTH))
    image = np.expand_dims(image, axis=0)
    predicted = model.predict(image)
    predicted = np.argmax(predicted)
    result = classes[predicted]
    str = "The cloth is a " + result + "."
    print(str)
    return str