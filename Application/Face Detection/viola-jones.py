import xml.etree.ElementTree as ET
from PIL import Image, ImageDraw
import numpy as np
import os

UNINIT = -99
FEAT_SIZE = 5
MAX_FEAT = 3
STAGE_PARAMS = 4

DEBUG = True

# PATH = os.path.dirname(os.path.abspath(__file__))
# os.path.insert(0, PATH)

def readHaarXML():
    global UNINIT, DEBUG
    # Load the XML file
    tree = ET.parse('haarcascade_frontalface_default.xml')
    root = tree.getroot()
    root = root[0] #root is now the first element of the tree which <cascade>

    #its size should be 25 (the number of stages)

    noOfStages = int(root.find("stageNum").text)
    stages = root.find("stages")

    stageParams = root.find("stageParams")
    maxWeakCount = int(stageParams.find("maxWeakCount").text)


    #The shape of trees is (noOfStages, maxWeakCount+1, STAGE_PARAMS)
    #The +1 is to use stage threshold as the first weak classifier
    trees = np.zeros((noOfStages,maxWeakCount+1,STAGE_PARAMS), dtype=np.float32)
    trees.fill(UNINIT)

    if DEBUG:
        print(f"noOfStages: {noOfStages}")
        print(f"maxWeakCount: {maxWeakCount}")
        print(f"trees.shape: {trees.shape}")

    noOfFeatures = 0

    # for each stage
    for i in range(noOfStages):
        stage = stages[i]
        noOfClassifiersInStage = int(stage.find("maxWeakCount").text)
        stageThreshold = float(stage.find("stageThreshold").text)
        weakClassifiers = stage.find("weakClassifiers")

        #Add stage threshold as the first weak classifier
        trees[i,0,0] = stageThreshold

        # for each weak classifier
        for j in range(noOfClassifiersInStage):

            noOfFeatures += 1

            #now we are in the weak classifier tag
            weakClassifier = weakClassifiers[j]
            internalNodes = weakClassifier.find("internalNodes")
            internalNodes = internalNodes.text.strip().split(" ")
            #Internal nodes are of the form:
            #1. node index in tree (not sure)
            #2. unknown
            #3. feature Index
            #4. threshold
            if internalNodes[0] != "0" and internalNodes[1] != "-1":
                print(f"Error in weak classifier {j} of stage {i}")
                

            featureIndex = int(internalNodes[2])
            threshold = float(internalNodes[3])

            
            leafValues = weakClassifier.find("leafValues")
            leafValues = leafValues.text.strip().split(" ")
            
            leftLeafValue = float(leafValues[0])
            rightLeafValue = float(leafValues[1])

            trees[i,j + 1,0] = featureIndex
            trees[i,j + 1,1] = threshold
            trees[i,j + 1,2] = leftLeafValue
            trees[i,j + 1,3] = rightLeafValue

    if DEBUG:
        print(f"First element of trees: {trees[0]}")

    # Read the features
    featuresArr = np.zeros((noOfFeatures,MAX_FEAT,FEAT_SIZE), dtype=np.float32)
    featuresArr.fill(UNINIT)

    features = root.find("features")
    if features is None:
        print("Error: features is None")
        return
    
    # for each feature
    for i in range(noOfFeatures):
        feature = features[i]
        rects = feature.find("rects")
        
        #The values in rects are of the form:
        #1. x (top left corner)
        #2. y (top left corner)
        #3. width
        #4. height
        #5. weight (it is used to compenstate the overlapping of rectangles)

        rectsArr = np.zeros((MAX_FEAT,FEAT_SIZE), dtype=np.float32)
        rectsArr.fill(UNINIT)
        for j in range(len(rects)):
            if len(rects) > 3:
                print(f"Error in feature {i}")
            rect = rects[j].text.strip().split(" ")
            rectsArr[j,0] = float(rect[0])
            rectsArr[j,1] = float(rect[1])
            rectsArr[j,2] = float(rect[2])
            rectsArr[j,3] = float(rect[3])
            rectsArr[j,4] = float(rect[4])       

        featuresArr[i] = rectsArr

    if DEBUG:
        print(f"featuresArr.shape: {featuresArr.shape}")
        print(f"Firis feature: {featuresArr[0]}")

    return trees, featuresArr

def imgPreprocessing(img):
    '''
    This function preprocesses the image
    '''
    #Convert it to grayscale
    img = img.convert("L")

    #Convert it to numpy array
    img = np.array(img)

    if np.max(img) == 1:
        img = img * 255

    #Zero mean and unit variance
    # img = (img - np.mean(img)) / np.std(img)

    return img

def calIntegralImage(img: np.ndarray) -> np.ndarray:
    '''
    This function calculates the integral image of an image
    '''

    global DEBUG

    #np.int_ is equivalent to np.int64
    ii = np.zeros((img.shape[0]+1,img.shape[1]+1), dtype = np.int_)
    ii[1:,1:] = np.cumsum(np.cumsum(img,axis=0, dtype = np.int_),axis=1, dtype = np.int_)


    if DEBUG:
        print(f"ii.shape: {ii.shape}")
        print(f"ii: {ii}")

    return ii

def applyFeature(integralImg:np.ndarray, feature: np.ndarray) -> float:
    '''
    This function applies a feature to an integral image
    A feature contains 2 or more rectangles
    '''
    finalSum = 0
    for i in range(len(feature)):
        if np.all(feature[i] == UNINIT):
            continue
        x = int(feature[i,0])
        y = int(feature[i,1])
        w = int(feature[i,2])
        h = int(feature[i,3])
        weight = float(feature[i,4])

        #The sum of the pixels in the rectangle is:
        #Bottom right corner - top right corner - bottom left corner + top left corner

        sum = integralImg[y+h,x+w] + integralImg[y,x] - integralImg[y,x+w] - integralImg[y+h,x]

        finalSum += weight * sum

    return finalSum    



def detectFace(img, tree, features):
    '''
    This function detects a face in an image
    '''
    
    #Preprocess the image
    img = imgPreprocessing(img)

    if DEBUG:
        print(f"img.shape: {img.shape}")
        print(f"img: {img}")

    #Compute the integral image
    ii = calIntegralImage(img)

    #For each stage
    for i in range(len(tree)):
        stageSum = 0

        stageThreshold = float(tree[i,0,1])
        #For each weak classifier
        for j in range(len(tree[i])):
            featureIndex = int(tree[i,j,0])
            threshold = float(tree[i,j,1])
            leftLeafValue = float(tree[i,j,2])
            rightLeafValue = float(tree[i,j,3])

            feature = features[featureIndex]

            featureSum = applyFeature(ii, feature)

            if featureSum < threshold:
                stageSum += leftLeafValue
            else:
                stageSum += rightLeafValue

        if stageSum < 0:
            return False

    return True


if __name__ == "__main__":
    stages, features = readHaarXML()

    #Read the image
    img = Image.open("oliTest.jpg")
    # img = Image.open("moazTest.jpg")
    

    #Detect the face
    print(detectFace(img, stages, features))

    

    
    




    




