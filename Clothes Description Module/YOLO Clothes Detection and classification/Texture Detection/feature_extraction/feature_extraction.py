import sys
sys.path.append('../')
from dataloader.dataloader import DataLoader

from imports import *

class FeatureExtractor:
    def __init__(self):
        self.data_loader = DataLoader(Path("../data/"))

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
        
        
    def extract_daisy_features(self, images):
        descs_features = []
        
        for image in images:
            image = self.data_loader.crop_center(image)
            descs = daisy(  image, 
                            step=180,
                            radius=58,
                            rings=2, 
                            histograms=8,
                            orientations=16,
                            visualize=False)
            descs = descs.flatten()
            descs_features.append(descs)
        descs_features = np.array(descs_features)
        return descs_features
        

