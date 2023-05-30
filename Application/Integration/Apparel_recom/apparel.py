import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os
import pathlib

PATH = pathlib.Path(__file__).parent



class ApparelRecommender:
    PRODUCT_ID = "product_id"
    TEXTURE = "texture"
    COLOR = "color"
    CLOTHES_TYPE = "clothes_type"
    
    def __init__(self):
        self._user_preferences = dict()

        self._apparel_data :dict[list] = dict()
        self._apparel_data[ApparelRecommender.PRODUCT_ID] = []
        self._apparel_data[ApparelRecommender.TEXTURE] = []
        self._apparel_data[ApparelRecommender.COLOR] = []
        self._apparel_data[ApparelRecommender.CLOTHES_TYPE] = []

        self._apparel_data_PD = None

        self._tfidf = TfidfVectorizer(stop_words='english')
        self._features_matrix = dict()
        self._cosine_similarities = dict()

    def addApparelData(self, product_id, texture, color, clothes_type) -> bool:

        

        #Check if the product_id is already present
        if product_id in self._apparel_data[ApparelRecommender.PRODUCT_ID]:
            return False

        #Add the data
        for key in self._apparel_data.keys():
            if key == ApparelRecommender.PRODUCT_ID:
                self._apparel_data[key].append(product_id)
            elif key == ApparelRecommender.TEXTURE:
                self._apparel_data[key].append(texture)
            elif key == ApparelRecommender.COLOR:
                self._apparel_data[key].append(color)
            elif key == ApparelRecommender.CLOTHES_TYPE:
                self._apparel_data[key].append(clothes_type)


        self._apparel_data_PD = pd.DataFrame(self._apparel_data)

        #Update the features matrix and cosine similarities based on the key which is the clothes type
        for key in self._user_preferences.keys():
            #key here represents the clothes type
            #get all the data for this clothes type
            data = self._apparel_data_PD[self._apparel_data_PD[ApparelRecommender.CLOTHES_TYPE] == key]
            #update the features matrix
            self._features_matrix[key] = self._tfidf.fit_transform(data[ApparelRecommender.TEXTURE] 
                                                                   + ' ' + data[ApparelRecommender.COLOR] 
                                                                   + ' ' + data[ApparelRecommender.CLOTHES_TYPE])

        return True

    def getTopRecommendations(self, product_id, n=5):

        
        # get the index of the product with the given id    
        product_index = self._apparel_data_PD.index[self._apparel_data_PD[ApparelRecommender.PRODUCT_ID] == product_id].tolist()[0]

        #Get the product's clothes type
        clothes_type = self._apparel_data_PD.iloc[product_index][ApparelRecommender.CLOTHES_TYPE]
        
        # get the cosine similarity scores for the product
        product_cosine_scores = self._cosine_similarities[clothes_type][product_index]
        
        # get the indices of the top n most similar products
        top_indices = product_cosine_scores.argsort()[::-1][:n+1]
        
        # remove the index of the original product from the list
        if product_index in top_indices :
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
        foundList = self._apparel_data_PD.index[(self._apparel_data_PD[ApparelRecommender.TEXTURE] == texture) 
                                                & (self._apparel_data_PD[ApparelRecommender.COLOR] == color) 
                                                & (self._apparel_data_PD[ApparelRecommender.CLOTHES_TYPE] == clothes_type)].tolist()

        if len(foundList) == 0:
            return (-1, len(self._apparel_data_PD[ApparelRecommender.PRODUCT_ID]))
        
        product_index = foundList[0]

        # return the top n most similar products
        return (self._apparel_data_PD.iloc[product_index][ApparelRecommender.PRODUCT_ID], 0)
    
    def setUserPreferences(self, texture, color, clothes_type):
        if clothes_type not in self._user_preferences.keys():
            self._user_preferences[clothes_type] = dict()
            self._user_preferences[clothes_type][ApparelRecommender.TEXTURE] = texture
            self._user_preferences[clothes_type][ApparelRecommender.COLOR] = color
        else:
            self._user_preferences[clothes_type][ApparelRecommender.TEXTURE] = texture
            self._user_preferences[clothes_type][ApparelRecommender.COLOR] = color


        if self._apparel_data_PD is None:
            self.addApparelData(0, texture, color, clothes_type)
        else:
            self.addApparelData(len(self._apparel_data_PD[ApparelRecommender.PRODUCT_ID]), texture, color, clothes_type)

    def saveUserPreference(self, filename):
        #Remove all colons from filename
        filename = filename.replace(':', '')
        filename = filename + '.pkl'
        pickle.dump(self._user_preferences, open(PATH.resolve()/ "pref" / filename, 'wb'))

    def loadUserPreference(self, filename) -> bool:
        filename = filename.replace(':', '')
        filename = filename + '.pkl'
        try:

            self._user_preferences = pickle.load(open(PATH.resolve()/ "pref" / filename, 'rb'))
            return True
        except Exception as e:
            print(e)
            return False
        
    def saveUserDataset(self,filename):
        #Remove all colons from filename
        filename = filename.replace(':', '')
        filename = filename + '.pkl'
        pickle.dump(self._apparel_data, open(PATH.resolve()/"dataset" / filename, 'wb'))

    def loadUserDataset(self, filename) -> bool:
        filename = filename.replace(':', '')
        filename = filename + '.pkl'
        try:

            self._apparel_data = pickle.load(open(PATH.resolve()/"dataset" / filename, 'rb'))
            self._apparel_data_PD = pd.DataFrame(self._apparel_data)
            self._features_matrix = self._tfidf.fit_transform(self._apparel_data_PD[ApparelRecommender.TEXTURE] + ' ' + self._apparel_data_PD[ApparelRecommender.COLOR] + ' ' + self._apparel_data_PD[ApparelRecommender.CLOTHES_TYPE])
            self._cosine_similarities = cosine_similarity(self._features_matrix)
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
    for i in range(len(apparel_data[ApparelRecommender.PRODUCT_ID])):
        apparel_recommender.addApparelData(apparel_data[ApparelRecommender.PRODUCT_ID][i], apparel_data[ApparelRecommender.TEXTURE][i], apparel_data[ApparelRecommender.COLOR][i], apparel_data[ApparelRecommender.CLOTHES_TYPE][i])

    product_id = apparel_recommender.getProductID('soft', 'red', 't-shirt')

    # get the top recommendations for product 1
    print(apparel_recommender.getTopRecommendations(product_id, 1))

    # # save the apparel recommender
    # apparel_recommender.save('apparel_recommender.pkl')

    # # load the apparel recommender
    # apparel_recommender.load('apparel_recommender.pkl')

    # # get the top recommendations for product 1
    # print(apparel_recommender.get_top_recommendations(product_id, 1))
