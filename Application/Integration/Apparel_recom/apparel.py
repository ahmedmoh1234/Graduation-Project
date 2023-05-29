import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os
import pathlib

PATH = pathlib.Path(__file__).parent



class ApparelRecommender:
    
    def __init__(self):
        self._user_preferences = None
        self._apparel_data = None
        self._apparel_data_PD = None
        self._tfidf = TfidfVectorizer(stop_words='english')
        self._features_matrix = None
        self._cosine_similarities = None

    def addApparelData(self, product_id, texture, color, clothes_type) -> bool:

        if self._apparel_data is None:
            self._apparel_data = dict()
            self._apparel_data['product_id'] = []
            self._apparel_data['texture'] = []
            self._apparel_data['color'] = []
            self._apparel_data['clothes_type'] = []

        #Check if the product_id is already present
        if product_id in self._apparel_data['product_id']:
            return False

        #Add the data
        for key in self._apparel_data.keys():
            if key == 'product_id':
                self._apparel_data[key].append(product_id)
            elif key == 'texture':
                self._apparel_data[key].append(texture)
            elif key == 'color':
                self._apparel_data[key].append(color)
            elif key == 'clothes_type':
                self._apparel_data[key].append(clothes_type)



        
        self._apparel_data_PD = pd.DataFrame(self._apparel_data)
       
        #update the features matrix
        self._features_matrix = self._tfidf.fit_transform(self._apparel_data_PD['texture'] + ' ' + self._apparel_data_PD['color'] + ' ' + self._apparel_data_PD['clothes_type'])

        #update the cosine similarities
        self._cosine_similarities = cosine_similarity(self._features_matrix)

        return True

    def getTopRecommendations(self, product_id, n=5):

        if self._apparel_data_PD is None:
            return "Apparel Recommendation not initialized"
        
        # get the index of the product with the given id    
        product_index = self._apparel_data_PD.index[self._apparel_data_PD['product_id'] == product_id].tolist()[0]
        
        # get the cosine similarity scores for the product
        product_cosine_scores = self._cosine_similarities[product_index]
        
        # get the indices of the top n most similar products
        top_indices = product_cosine_scores.argsort()[::-1][:n+1]
        
        # remove the index of the original product from the list
        if product_index in top_indices:
            top_indices = list(top_indices)
            top_indices.remove(product_index)
        
        if len(top_indices) == 0:
            return "There isn't enough data to make a recommendation"
        
        # return the top n most similar products
        return self._apparel_data_PD.iloc[top_indices]
    
    def getProductID(self, texture, color, clothes_type):
        if self._apparel_data_PD is None:
            return (-2, 0)
        


        # get the index of the product with the given id    
        foundList = self._apparel_data_PD.index[(self._apparel_data_PD['texture'] == texture) & (self._apparel_data_PD['color'] == color) & (self._apparel_data_PD['clothes_type'] == clothes_type)].tolist()

        if len(foundList) == 0:
            return (-1, len(self._apparel_data_PD['product_id']))
        
        product_index = foundList[0]

        #if not found, return -1 and new product ID
        if product_index is None:
            return (-1, len(self._apparel_data_PD['product_id']))
        
        # return the top n most similar products
        return (self._apparel_data_PD.iloc[product_index]['product_id'], 0)
    
    def setUserPreferences(self, texture, color, clothes_type):
        self._user_preferences = {
            'texture': texture,
            'color': color,
            'clothes_type': clothes_type
        }

        self.addApparelData(len(self._apparel_data_PD['product_id']), texture, color, clothes_type)

    def saveUserPreference(self, filename):
        #Remove all colons from filename
        filename = filename.replace(':', '')
        filename = filename + '.pkl'
        pickle.dump(self._user_preferences, open(PATH.resolve() / filename, 'wb'))

    def loadUserPreference(self, filename) -> bool:
        filename = filename.replace(':', '')
        filename = filename + '.pkl'
        try:

            self._user_preferences = pickle.load(open(PATH.resolve() / filename, 'rb'))
            return True
        except Exception as e:
            print(e)
            return False
        

    

        


if __name__ == '__main__':


    # define some example data
    apparel_data = {
        'product_id': [1, 2, 3, 4, 5],
        'texture': ['soft', 'rough', 'smooth', 'silky', 'soft'],
        'color': ['red', 'blue', 'black', 'green', 'red'],
        'clothes_type': ['sweater', 'jeans', 't-shirt', 'dress', 't-shirt']
    }

    # create an instance of the ApparelRecommender class
    apparel_recommender = ApparelRecommender()

    # add the apparel data to the recommender
    for i in range(len(apparel_data['product_id'])):
        apparel_recommender.addApparelData(apparel_data['product_id'][i], apparel_data['texture'][i], apparel_data['color'][i], apparel_data['clothes_type'][i])

    product_id = apparel_recommender.getProductID('soft', 'red', 't-shirt')

    # get the top recommendations for product 1
    print(apparel_recommender.getTopRecommendations(product_id, 1))

    # # save the apparel recommender
    # apparel_recommender.save('apparel_recommender.pkl')

    # # load the apparel recommender
    # apparel_recommender.load('apparel_recommender.pkl')

    # # get the top recommendations for product 1
    # print(apparel_recommender.get_top_recommendations(product_id, 1))
