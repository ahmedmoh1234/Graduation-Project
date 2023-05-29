import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os
import pathlib

PATH = pathlib.Path(__file__).parent



class ApparelRecommender:
    apparel_data = None,
    apparel_data_PD = None,
    tfidf = None,
    features_matrix = None,
    cosine_similarities = None,
    
    def __init__(self):
        self.apparel_data = None
        self.apparel_data_PD = None
        self.tfidf = TfidfVectorizer(stop_words='english')
        self.features_matrix = None
        self.cosine_similarities = None

    def add_apparel_data(self, product_id, texture, color, clothes_type):

        if self.apparel_data is None:
            self.apparel_data = dict()
            self.apparel_data['product_id'] = []
            self.apparel_data['texture'] = []
            self.apparel_data['color'] = []
            self.apparel_data['clothes_type'] = []

        #Check if the product_id is already present
        if product_id in self.apparel_data['product_id']:
            return

        #Add the data
        for key in self.apparel_data.keys():
            if key == 'product_id':
                self.apparel_data[key].append(product_id)
            elif key == 'texture':
                self.apparel_data[key].append(texture)
            elif key == 'color':
                self.apparel_data[key].append(color)
            elif key == 'clothes_type':
                self.apparel_data[key].append(clothes_type)



        
        self.apparel_data_PD = pd.DataFrame(self.apparel_data)
       
        #update the features matrix
        self.features_matrix = self.tfidf.fit_transform(self.apparel_data_PD['texture'] + ' ' + self.apparel_data_PD['color'] + ' ' + self.apparel_data_PD['clothes_type'])

        #update the cosine similarities
        self.cosine_similarities = cosine_similarity(self.features_matrix)

    def get_top_recommendations(self, product_id, n=5):

        if self.apparel_data_PD is None:
            return "Apparel Recommendation not initialized"
        
        # get the index of the product with the given id    
        product_index = self.apparel_data_PD.index[self.apparel_data_PD['product_id'] == product_id].tolist()[0]
        
        # get the cosine similarity scores for the product
        product_cosine_scores = self.cosine_similarities[product_index]
        
        # get the indices of the top n most similar products
        top_indices = product_cosine_scores.argsort()[::-1][:n+1]
        
        # remove the index of the original product from the list
        if product_index in top_indices:
            top_indices = list(top_indices)
            top_indices.remove(product_index)
        
        if len(top_indices) == 0:
            return "No similar products found"
        
        # return the top n most similar products
        return self.apparel_data_PD.iloc[top_indices]
    
    def getProductID(self, texture, color, clothes_type):
        if self.apparel_data_PD is None:
            return (-2, 0)
        


        # get the index of the product with the given id    
        foundList = self.apparel_data_PD.index[(self.apparel_data_PD['texture'] == texture) & (self.apparel_data_PD['color'] == color) & (self.apparel_data_PD['clothes_type'] == clothes_type)].tolist()

        if len(foundList) == 0:
            return (-1, len(self.apparel_data_PD['product_id']))
        
        product_index = foundList[0]

        #if not found, return -1 and new product ID
        if product_index is None:
            return (-1, len(self.apparel_data_PD['product_id']))
        
        # return the top n most similar products
        return (self.apparel_data_PD.iloc[product_index]['product_id'], 0)
    
    def save(self, filename):
        #Remove all colons from filename
        filename = filename.replace(':', '')
        filename = filename + '.pkl'
        pickle.dump(self.apparel_data, open(PATH.resolve() / filename, 'wb'))

    def load(self, filename) -> bool:
        filename = filename.replace(':', '')
        filename = filename + '.pkl'
        try:

            self.apparel_data = pickle.load(open(PATH.resolve() / filename, 'rb'))
            self.apparel_data_PD = pd.DataFrame(self.apparel_data)
            self.features_matrix = self.tfidf.fit_transform(self.apparel_data_PD['texture'] + ' ' + self.apparel_data_PD['color'] + ' ' + self.apparel_data_PD['clothes_type'])
            self.cosine_similarities = cosine_similarity(self.features_matrix)
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
        apparel_recommender.add_apparel_data(apparel_data['product_id'][i], apparel_data['texture'][i], apparel_data['color'][i], apparel_data['clothes_type'][i])

    product_id = apparel_recommender.getProductID('soft', 'red', 't-shirt')

    # get the top recommendations for product 1
    print(apparel_recommender.get_top_recommendations(product_id, 1))

    # # save the apparel recommender
    # apparel_recommender.save('apparel_recommender.pkl')

    # # load the apparel recommender
    # apparel_recommender.load('apparel_recommender.pkl')

    # # get the top recommendations for product 1
    # print(apparel_recommender.get_top_recommendations(product_id, 1))
