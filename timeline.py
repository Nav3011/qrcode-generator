import cv2
import time
import os

def saveImage(image):
	filename = "history/image_{0}.jpg".format(int(time.time()))
	# filename = "/timeline/image_{0}.jpg".format(int(time.time()))
	current_directory = os.getcwd()
	print("file", os.path.join(current_directory, filename))
	cv2.imwrite(os.path.join(current_directory, filename), image)
	cv2.imwrite(filename, image)

# saveImage("image")