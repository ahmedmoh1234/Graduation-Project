import sys
sys.path.append('../')

from imports import *

class FeatureExtractor:
    def __init__(self):
        pass

    def extract_glcm_features(self,images):
        glcm_features = []

        # Loop over each image
        for gray_image in images:

            # Calculate GLCM matrix
            glcm = graycomatrix(gray_image, distances=[1], angles=[0], symmetric=True, normed=True)

            # Extract desired GLCM properties
            contrast = graycoprops(glcm, 'contrast')[0][0]
            dissimilarity = graycoprops(glcm, 'dissimilarity')[0][0]
            homogeneity = graycoprops(glcm, 'homogeneity')[0][0]
            energy = graycoprops(glcm, 'energy')[0][0]
            correlation = graycoprops(glcm, 'correlation')[0][0]

            # Append the features to the vector
            glcm_features.append([contrast, dissimilarity, homogeneity, energy, correlation])

        # Convert the list to a numpy array
        glcm_features = np.array(glcm_features)

        return glcm_features
        

