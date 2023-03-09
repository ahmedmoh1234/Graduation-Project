import os
from PIL import Image
import random
from PIL import ImageDraw

supportedExtensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp']
DIM = 312
imgNo = 0
PAD_COLOR = (0, 0, 0)

imgArr = []
boxArr = ["0    0.5    0.5    0.17628    0.641025",
          "0    0.48717    0.48717    0.21153    0.78846",
          "0    0.5    0.5    0.26923    0.98076",
          "0    0.5    0.50641    0.21794    0.80128"]
NO_OF_IMGS_REQ = 2000

for file in os.listdir('.'):
    if os.path.splitext(file)[1] in supportedExtensions:
        img = Image.open(file)
        width, height = img.size
        if width != height:
            if width > height:
                #pad the height
                paddedImg = Image.new('RGB', (width, width), PAD_COLOR)
                paddedImg.paste(img, (0, int((width - height) / 2)))
                img = paddedImg

            else:
                #pad the width
                paddedImg = Image.new('RGB', (height, height), PAD_COLOR)
                paddedImg.paste(img, (int((height - width) / 2), 0))
                img = paddedImg
        if width != DIM and width != DIM:
            img = img.resize((DIM, DIM), Image.ANTIALIAS)
        
        # width, height = img.size
        # center = (156, 158)
        # objWidth = 68
        # objjHeight = 250
        # #draw bounding box
        # draw = ImageDraw.Draw(img)
        # draw.rectangle(((center[0] - objWidth/2, center[1] - objjHeight/2), (center[0] + objWidth/2, center[1] + objjHeight/2)), outline="red")
        
        # img.show()
        
        imgArr.append(img)

noPerImg = NO_OF_IMGS_REQ / len(imgArr)
imgsNo = [noPerImg for i in range(len(imgArr))]

while sum(imgsNo) != 0:
    index = random.randint(0,3)
    if (imgsNo[index] != 0):
        imgArr[index].save("finalImages/img"+str(imgNo)+".png")
        imgsNo[index] -= 1
        with open("finalLabels/img"+str(imgNo)+".txt", "w") as text_file:
            text_file.write(boxArr[index])
        imgNo += 1

