import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import pathlib
import logging

PATH = pathlib.Path(__file__).parent

logger = logging.getLogger(__name__)

#check if loggers are already set
if not logger.hasHandlers():
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    file_handler = logging.FileHandler(PATH.resolve() / "apparel.log")
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

class Rule():
        
    textStr = "texture"
    colorStr = "color"
    clothesTypeStr = "clothes_type"
    
    def __init__(self, op1:tuple[str,str,str], op2:tuple[str,str,str]):
        self._topClothes = None
        self._bottomClothes = None
        self.setRule(op1, op2)

    def setRule(self, op1:tuple[str,str,str], op2:tuple[str,str,str]):
        self._topClothes = op1
        self._bottomClothes = op2
       
        

    def __call__(self, topClothes, bottomClothes):
        if self._topClothes == None or self._bottomClothes == None :
            return False
        
        for i in range(len(self._topClothes)):
            if self._topClothes[i] == None or self._bottomClothes[i] == None:
                continue

            if self._topClothes[i].strip().lower() != topClothes[i].strip().lower() and self._topClothes[i].strip().lower() != bottomClothes[i].strip().lower():
                return False
            
        return True

        
    def __str__(self) -> str:
        return f"Rule: Top = {self._topClothes},\t Bottom =  {self._bottomClothes}"
     
class FashionModule():

    def __init__(self):
        self._topClothes = None
        self._bottomClothes = None
        self._rules = []

    def setTopClothes(self, texture, color, clothes_type):
        self._topClothes = (texture, color, clothes_type)
        logger.info(f"Top clothes set: texture: {texture}, color: {color}, clothes_type: {clothes_type}")

    def setBottomClothes(self, texture, color, clothes_type):
        self._bottomClothes = (texture, color, clothes_type)
        logger.info(f"Bottom clothes set: texture: {texture}, color: {color}, clothes_type: {clothes_type}")

    def addRule(self,rule):
        self._rules.append(rule)
        logger.info(f"Rule added: {str(rule)}")

    def checkRules(self) -> bool:

        for rule in self._rules:
            if rule(self._topClothes, self._bottomClothes):
                return True
        return False
    
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
        self._features_matrix = None
        self._cosine_similarities = None

        self._fashionModule = FashionModule()

        rules = []

        for rule in rules:
            self._fashionModule.addRule(rule)

        logger.info("ApparelRecommender initialized")

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

        #update the dataframe
        self._apparel_data_PD = pd.DataFrame(self._apparel_data)
        
        #update the features matrix
        self._features_matrix = self._tfidf.fit_transform(self._apparel_data_PD[ApparelRecommender.TEXTURE] 
                                                          + ' ' + self._apparel_data_PD[ApparelRecommender.COLOR] 
                                                          + ' ' + self._apparel_data_PD[ApparelRecommender.CLOTHES_TYPE])
            
        #update the cosine similarities
        self._cosine_similarities = cosine_similarity(self._features_matrix)

        logger.info(f"Added product_id: {product_id}, texture: {texture}, color: {color}, clothes_type: {clothes_type}")

        return True

    def getTopRecommendations(self, product_id):
        '''
        Returns the top n most similar products to a given product id
        '''

        productType = self._apparel_data_PD.iloc[product_id][ApparelRecommender.CLOTHES_TYPE]
        productTexture = self._apparel_data_PD.iloc[product_id][ApparelRecommender.TEXTURE]
        productColor = self._apparel_data_PD.iloc[product_id][ApparelRecommender.COLOR]

        # get the index of the product with the given id
        product_index = self._apparel_data_PD.index[(self._apparel_data_PD[ApparelRecommender.TEXTURE] == productTexture) 
                                                    & (self._apparel_data_PD[ApparelRecommender.COLOR] == productColor)
                                                    & (self._apparel_data_PD[ApparelRecommender.CLOTHES_TYPE] == productType)].tolist()[0]
        
        # get the cosine similarity scores for the product
        product_cosine_scores = self._cosine_similarities[product_index]
        
        # get the indices of the top n most similar products
        top_indices = product_cosine_scores.argsort()[::-1]
        
        
        print(top_indices)

        if len(top_indices) == 0:
            logger.info("There isn't enough data to make a recommendation")
            return "There isn't enough data to make a recommendation"
        
        for ind in top_indices:
            if productType == self._apparel_data_PD.iloc[ind][ApparelRecommender.CLOTHES_TYPE]:
                return self._apparel_data_PD.iloc[ind]

        logger.info(f"There isn't enough clothes of type {productType} to make a recommendation")
        return "There isn't enough data to make a recommendation"
    
    def getProductID(self, texture, color, clothes_type):
        '''
        Returns a tuple of either the product_id and 0 if the product is found 
        or -1 and new product id if the product is not found
        or -2 and 0 if there is no data
        '''
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

        logger.info(f"User preferences updated: texture: {texture}, color: {color}, clothes_type: {clothes_type}")

    def saveUserPreference(self, filename):
        #Remove all colons from filename
        filename = filename.replace(':', '')
        filename = filename + '.pkl'
        pickle.dump(self._user_preferences, open(PATH.resolve()/ "pref" / filename, 'wb'))

        logger.info(f"User preferences saved to {filename}")

    def loadUserPreference(self, filename) -> bool:
        filename = filename.replace(':', '')
        filename = filename + '.pkl'
        try:
            self._user_preferences = pickle.load(open(PATH.resolve()/ "pref" / filename, 'rb'))
            logger.info(f"User preferences loaded from {filename}")
            return True
        except Exception as e:
            logger.info(f"User preferences could NOT be loaded from {filename}")
            return False
        
    def saveUserDataset(self,filename):
        #Remove all colons from filename
        filename = filename.replace(':', '')
        filename = filename + '.pkl'
        pickle.dump(self._apparel_data, open(PATH.resolve()/"dataset" / filename, 'wb'))

        logger.info(f"User dataset saved to {filename}")

    def loadUserDataset(self, filename) -> bool:
        filename = filename.replace(':', '')
        filename = filename + '.pkl'
        try:

            self._apparel_data = pickle.load(open(PATH.resolve()/"dataset" / filename, 'rb'))
            self._apparel_data_PD = pd.DataFrame(self._apparel_data)
            self._features_matrix = self._tfidf.fit_transform(self._apparel_data_PD[ApparelRecommender.TEXTURE] + ' ' + self._apparel_data_PD[ApparelRecommender.COLOR] + ' ' + self._apparel_data_PD[ApparelRecommender.CLOTHES_TYPE])
            self._cosine_similarities = cosine_similarity(self._features_matrix)
            logger.info(f"User dataset loaded from {filename}")
            return True
        except Exception as e:
            logger.info(f"User dataset could NOT be loaded from {filename}")
            return False




if __name__ == '__main__':

    #create a rule
    rules = [Rule(("cotton", "green",None),("cotton", "black", "pants")),
             Rule(("silk", None,None),(None, "black", "pants")),
   ]

    #create a fashion module
    fashionModule = FashionModule()

    #add the rule to the fashion module
    for rule in rules:
        fashionModule.addRule(rule)

    #set the top clothes
    fashionModule.setTopClothes("silk", "white", "t-shirt")

    #set the bottom clothes
    fashionModule.setBottomClothes("jeans", "black", "pants")

    #check the rules
    print(fashionModule.checkRules())
