import sys
sys.path.append('../')

from imports import *


class FeatureSelector:
    def __init__(self) -> None:
        pass

    def extract_pca_features(self, images, load=False, num_pca_components=0.95):
        
        # image_vectors = []
        # for image in images:
        #     image_vectors.append(image.flatten())
        # image_vectors = np.array(image_vectors)
        
        image_vectors = images
        
        if load:
            pca = pickle.load(open("pca.pkl", "rb"))
            pca_features = pca.transform(image_vectors)
        else:
            print("Creating new PCA model...")
            pca = PCA(n_components = num_pca_components, svd_solver = 'full')
            pca.fit(image_vectors)

            pca_features = pca.transform(image_vectors)
            pickle.dump(pca, open("pca.pkl", "wb"))

        pca_features = np.array(pca_features)
        return pca_features
        
    def extract_daisy_features(self, images):
        descs_features = []
        
        for image in images:
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
        
    def test_pca(self,img, pca):
        image_vector = img.flatten()
        pca_features = pca.transform(np.array([image_vector]))
        return pca_features
        
