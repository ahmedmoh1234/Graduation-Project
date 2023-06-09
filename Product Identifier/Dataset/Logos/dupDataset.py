

def repeatDataset():
    import os
    from PIL import Image
    import random
    import time 

    parentDir = '/content/datasets/train'
    #get all folders in path
    folders = os.listdir(parentDir)

    print(f"folders are : {folders}")
    

    for folder in folders:

        dataImgPath = f'{parentDir}/{folder}'

        NO_OF_IMGS_REQ = 5200
        imgNo = len(os.listdir(dataImgPath))

        currentImgNo = imgNo + 1

        imgArr = sorted(os.listdir(dataImgPath))

        imgArr = [i for i in imgArr if i not in [".ipynb_checkpoints"]]

        noPerImg = NO_OF_IMGS_REQ // imgNo
        
        noPerImgArr = [noPerImg] * imgNo

        #add remainder to last element
        noPerImgArr[-1] += NO_OF_IMGS_REQ % imgNo

        print(f"Number of images = {noPerImgArr}")


        print(f"imgArr = {imgArr}")



        lastTime = time.time()

        #Add images to array
        while currentImgNo < NO_OF_IMGS_REQ:
            
            #select random no from imgNo
            randNo = random.randint(0, imgNo-1)

            #check if noPerImgArr[randNo] is 0
            if noPerImgArr[randNo] == 0:
                continue

            #decrement noPerImgArr[randNo]
            noPerImgArr[randNo] -= 1
            
            #select random image
            imgName = Image.open(dataImgPath + '/' + imgArr[randNo]).convert("RGB")

            #save image
            imgName.save(dataImgPath + '/' + str(currentImgNo) + '.jpg')

            #close image
            imgName.close()

            #increment currentImgNo
            currentImgNo += 1



            #progress bar updates every 1 second
            curTime = time.time()
            if curTime - lastTime > 2:

                #clear line
                print('\r', end='')

                #print progress
                print('Progress: ' + str(currentImgNo) + '/' + str(NO_OF_IMGS_REQ), end='')
                lastTime = curTime


    print('Finished repeating dataset')


repeatDataset()
