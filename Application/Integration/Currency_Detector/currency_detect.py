from matplotlib import pyplot as plt
import os
# from playsound import playsound
import cv2
import subprocess
from gtts import gTTS
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
# print(50*'-')
# print(sys.path)
# print(50*'-')
from currency_utils import resize_img
# from utils import *

def createAbsolutePaths(relativePath):
    absPath = os.path.dirname(__file__)
    absPath = absPath.replace('\\', '/')
    absPath = absPath + relativePath
    return absPath


def currency_detector(currencyImg):
	max_val = 8
	max_pt = -1
	max_kp = 0

	orb = cv2.ORB_create()
	# orb is an alternative to SIFT

	# test_img = read_img('files/test_100_2.jpg')
	# test_img = read_img('files/test_100_1.jpg')
	# test_img = read_img('files/test_20LE_1.jpg')
	# test_img = read_img('files/test_50_1.jpg')
	#test_img = read_img('files/test_100_3.jpg')
	#test_img = read_img('files/test_20_4.jpg')
	test_img = currencyImg

	# resizing must be dynamic
	original = resize_img(test_img, 0.4)
	# original = test_img
	# display('original', original)

	# keypoints and descriptors
	# (kp1, des1) = orb.detectAndCompute(test_img, None)
	(kp1, des1) = orb.detectAndCompute(test_img, None)

	# training_set = ['files/20.jpg', 'files/50.jpg', 'files/100.jpg', 'files/500.jpg']
	# training_set = ['files/20LE_1.jpg','files/20LE_2.jpg', 'files/50.jpg', 'files/100.jpg', 'files/500.jpg']
	training_set = [createAbsolutePaths('/files/20LE_1.jpg'),createAbsolutePaths('/files/20LE_2.jpg')]

	for i in range(0, len(training_set)):
		# train image
		train_img = cv2.imread(training_set[i])
		
		# print(50*'-')
		# print('train_img ', train_img.shape)
		# print(50*'-')

		# plt.imshow(train_img)
		# plt.show()
		(kp2, des2) = orb.detectAndCompute(train_img, None)

		# brute force matcher
		bf = cv2.BFMatcher()
		print('des2 ', des2.shape)
		all_matches = bf.knnMatch(des1, des2, k=2)

		good = []
		# give an arbitrary number -> 0.789
		# if good -> append to list of good matches
		for (m, n) in all_matches:
			if m.distance < 0.789 * n.distance:
				good.append([m])

		if len(good) > max_val:
			max_val = len(good)
			max_pt = i
			max_kp = kp2

		print(i, ' ', training_set[i], ' ', len(good))

	if max_val != 8:
		print(training_set[max_pt])
		print('good matches ', max_val)

		train_img = cv2.imread(training_set[max_pt])
		img3 = cv2.drawMatchesKnn(test_img, kp1, train_img, max_kp, good, 4)
		
		#Detect if training_set[max_pt] is None
		
		note = str(training_set[max_pt]).split('/')[-1].split('.')[0]
		if(note==None):
			note = 'None'
		print('\nDetected denomination: LE. ', note)

		# audio_file = 'audio/{}.mp3'.format(note)
		# audio_file = "value.mp3"
		# tts = gTTS(text=speech_out, lang="en")
		# tts.save(audio_file)
		# return_code = subprocess.call(["afplay", audio_file])
		# playsound(audio_file)
		# (plt.imshow(img3), plt.show())

		return note

	else:
		print('No Matches')
		return 'None'