

def repeatDataset():
    import os
    from PIL import Image
    import random
    import time 

    dataImgPath = '/content/datasets/waterBottles/images'
    dataLabelsPath = '/content/datasets/waterBottles/labels'

    NO_OF_IMGS_REQ = 5200
    imgNo = len(os.listdir(dataImgPath))

    currentImgNo = imgNo + 1

    imgArr = sorted(os.listdir(dataImgPath))
    labelArr = sorted(os.listdir(dataLabelsPath))

    print(f"imgArr = {imgArr}")

    print(f"labelArr = {labelArr}")

    lastTime = time.time()

    #Add images to array
    while currentImgNo < NO_OF_IMGS_REQ:
        
        #select random no from imgNo
        randNo = random.randint(0, imgNo-1)
        
        #select random image
        imgName = Image.open(dataImgPath + '/' + imgArr[randNo])

        #select random label
        labelName = open(dataLabelsPath + '/' + labelArr[randNo], 'r')

        #save image
        imgName.save(dataImgPath + '/' + str(currentImgNo) + '.jpg')

        #save label
        label = open(dataLabelsPath + '/' + str(currentImgNo) + '.txt', 'w')
        label.write(labelName.read())
        label.close()

        #increment currentImgNo
        currentImgNo += 1

        #close labelName
        labelName.close()

        #progress bar updates every 1 second
        curTime = time.time()
        if curTime - lastTime > 1:

            #clear line
            print('\r', end='')

            #print progress
            print('Progress: ' + str(currentImgNo) + '/' + str(NO_OF_IMGS_REQ))


    print('Finished repeating dataset')


repeatDataset()
