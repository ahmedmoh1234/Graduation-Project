import cv2
from time import sleep
import requests
import io
import json
import os
import random


def document_scanner(img):

    # key = cv2.waitKey(1)
    # webcam = cv2.VideoCapture(0)
    # sleep(2)

    # print("For Recognize Image PRESS 'S'\n"
    #     "For QUIT PRESS 'Q\n"
    #     "After run time if 'images.jpg' is still visible,Please re-run the program.\n")

    # while True:
    #     try:
    #         check, frame = webcam.read()
    #         print(check)  # prints true as long as the webcam is running
    #         print(frame)  # prints matrix values of each framecd
    #         cv2.imshow("Capturing", frame)
    #         key = cv2.waitKey(1)
    #         if key == ord('s'):
    #             # im = cv2.imread('images.jpg', cv2.IMREAD_ANYCOLOR)
    #             cv2.imwrite(filename='images.jpg', img=frame)
    #             # cv2.imshow("Captured Image", )
    #             r = random.randint(1, 20000000)
    #             img_file = 'images' + str(r) + '.jpg'
    #             # img_file = 'image.png'
    #             im = cv2.imread('image1.png', cv2.IMREAD_ANYCOLOR)
    #             cv2.imwrite(filename='data/' + img_file, img=frame)
    #             webcam.release()
    #             print("Processing image...")
    #             # img_ = cv2.imread('images.jpg', cv2.IMREAD_ANYCOLOR)
    #             img_ = cv2.imread('images.jpg', cv2.IMREAD_ANYCOLOR)
    #             print("Image saved!")
    #             cv2.destroyAllWindows()
    #             break

    #         elif key == ord('q'):
    #             webcam.release()
    #             cv2.destroyAllWindows()
    #             break

    #     except KeyboardInterrupt:
    #         print("Turning off camera.")
    #         webcam.release()
    #         print("Camera off.")
    #         print("Program ended.")
    #         cv2.destroyAllWindows()
    #         break

    # sleep(2)
    # resim = "images.jpg"
    resim = "images.jpg"
    # img = cv2.imread(resim)
    # imshow = cv2.imshow("img2", img)

    print("Picture is Detected")

    api = img

    # Ocr
    url_api = "https://api.ocr.space/parse/image"
    _, compressedimage = cv2.imencode(".jpg", api, [1, 90])
    file_bytes = io.BytesIO(compressedimage)

    result = requests.post(url_api,
                        files={resim: file_bytes},
                        data={"apikey": "helloworld",
                                "language": "eng"})

    result = result.content.decode()
    print(f'RESULT: {result}')
    result = json.loads(result)
    if (result == None):
        print("Text is not detected")
        text_detected = "Text is not detected"
        return text_detected
    parsed_results = result.get("ParsedResults")[0]
    if(parsed_results == None):
        print("Text is not detected")
        text_detected = "Text is not detected"
        return text_detected
    text_detected = parsed_results.get("ParsedText")
    print(text_detected)
    print("Operation is successful")
    if (text_detected == ""):
        print("Text is not detected")
        text_detected = "Text is not detected"
    if (text_detected == " "):
        print("Text is not detected")
        text_detected = "Text is not detected"
    if (text_detected == None):
        print("Text is not detected")
        text_detected = "Text is not detected"
    return text_detected
    # print("Text is writing to file...")
    # f = open("text_detected.txt", "a+")
    # f.write(text_detected)
    # f.close()


    # cv2.imshow("roi", api)
    # cv2.imshow("Img", img)
    # cv2.waitKey(0)
    # os.remove(resim)
