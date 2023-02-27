from facenet_pytorch import InceptionResnetV1, MTCNN
from PIL import Image
import torch
import os
from torchvision import datasets
from torch.utils.data import DataLoader


relativePath = './Face_Recognition'

class FaceDetector:
    #MTCNN (Multi-Task Cascaded Convolutional Networks) for face detection and alignment
    mtcnn = MTCNN(image_size=160, margin=0, min_face_size=20) #keep margin 0 for better accuracy

    # Load a pretrained model (requires internet the first time). Trained on VGGFace2 dataset.
    # Both pretrained models were trained on 160x160 px images, so will perform best if applied to images resized to this shape. For best results, images should also be cropped to the face using MTCNN
    pretrainedModel = InceptionResnetV1(pretrained='vggface2').eval()

    trainedModelPath = ""

    def __init__(self) :
        if "trainedModel" in os.listdir(relativePath):
            if os.listdir(relativePath + "/trainedModel") != []:
                self.trainedModelPath = relativePath + "/trainedModel/" + os.listdir(relativePath + "/trainedModel")[0]
            else:
                self.trainedModelPath = self.train()
        else:
            os.mkdir(relativePath + "/trainedModel")
            self.trainedModelPath = self.train()


    def train(self, trainingOutput=relativePath + "/trainedModel", datasetPath = relativePath + "/images"):
        def collate_fn(x):
            return x[0]
        #This will load images into dataset.
        #Images should be in a folder named "images" in the same directory as this file.
        #inside the "images" folder, there should be a folder for each person with their name as the folder name, and each person's folder should contain their images.
        dataset = datasets.ImageFolder(datasetPath)
        #dataset is a dictionary with the key being the name of the person and the value being their ID
        
        names = list(dataset.class_to_idx.keys()) #list of names of people in the photos folder
        namesStr = "" #string of names of people in the photos folder
        for name in names:
            namesStr += name + "_"
            #Add the no of photos of each person to the trained model file name
            namesStr += str(len(os.listdir(datasetPath + "/" + name))) + "_"
            

        namesStr = namesStr.rstrip("_")

        namesStr += ".pt"

        # print(f"namesStr: {namesStr}")

        if namesStr in os.listdir(trainingOutput): #if the file name is already created, then no need to create it again
            return ""
        
        # print("Training...")

        #Swap the key and value of the dictionary
        id_to_name = {v: k for k, v in dataset.class_to_idx.items()}
        loader = DataLoader(dataset, collate_fn=collate_fn)

        name_list = [] # list of names corrospoing to cropped photos
        embedding_list = [] # list of embeding matrix after conversion from cropped faces to embedding matrix using resnet

        for img, idx in loader:
            face, prob = self.mtcnn(img, return_prob=True) 
            if face is not None and prob>0.90: # if face detected and porbability > 90%
                emb = self.pretrainedModel(face.unsqueeze(0)) # passing cropped face into resnet model to get embedding matrix
                embedding_list.append(emb.detach()) # resulten embedding matrix is stored in a list
                name_list.append(id_to_name[idx]) # names are stored in a list

        data = [embedding_list, name_list]

        # #Creating a file name from names of people in the photos folder
        # fileName = ""
        # #remove duplicates from name_list
        # name_list = list(dict.fromkeys(name_list))

        # for name in name_list:
        #     fileName += name + "_" 

        # fileName = fileName.rstrip("_")

        outputFinal = trainingOutput +"/" +  namesStr
        # print(f"fileName: {outputFinal}")
        torch.save(data, outputFinal ) # saving data.pt file

        return outputFinal


    def faceMatch(self,img, threshold): # img_path= lcation of photo, data_path= location of data.pt 
        # getting embedding matrix of the given img
        # img = Image.open(img_path)
        face, prob = self.mtcnn(img, return_prob=True) # returns cropped face and probability
        emb = self.pretrainedModel(face.unsqueeze(0)).detach() # detech is to make required gradient false
        
        # print(f"Loading {data_path}")
        # load the .pt file
        if self.trainedModelPath != "":
            saved_data = torch.load(self.trainedModelPath)
        else:
            # print("No trained model found, training...")
            self.trainedModelPath = self.train()
            saved_data = torch.load(self.trainedModelPath)

        embedding_list = saved_data[0] # getting embedding data
        name_list = saved_data[1] # getting list of names
        dist_list = [] # list of matched distances, minimum distance is used to identify the person
        
        for idx, emb_db in enumerate(embedding_list):
            dist = torch.dist(emb, emb_db).item()
            dist_list.append(dist)
            
        idx_min = dist_list.index(min(dist_list))

        if min(dist_list)>threshold:
            return "Unknown"
        else:
            return str(name_list[idx_min])


    def getAvailableFaces(self):    #Returns a string of all the available faces separated by commas
        names = ""
        for name in os.listdir(relativePath + "/images"):
            names += name + ","
        names = names.rstrip(",")
        return names


if __name__ == "__main__":
    print('My Path: ' + os.getcwd())
    
    fd = FaceDetector()
    
    result = fd.faceMatch('naderTest.jpg',1)

    print(f"Faced matched with {result}")

    print(fd.getAvailableFaces())
