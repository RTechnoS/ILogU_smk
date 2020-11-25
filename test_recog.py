import numpy as np
import cv2 as cv
import os
import fungsi

#muka = fungsi.faceDetect('haar')

def face_detection(image):
    image_gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    haar_classifier = cv.CascadeClassifier('model/haarcascade_frontalface_default.xml')
    face = haar_classifier.detectMultiScale(image_gray, scaleFactor=1.3, minNeighbors=7)
    (x,y,w,h) = face[0]
    print(image_gray[y:y+w, x:x+h], face[0])
    return image_gray[y:y+w, x:x+h], face[0]


def prepare_data(data_path):
	folders = os.listdir(data_path)
	labels = []
	faces = []
	for folder in folders:
		print(folder)
		label = folder
		
	training_images_path = data_path + '/' + folder

	for image in os.listdir(training_images_path):
		image_path = training_images_path + '/' + image
	training_image = cv.imread(image_path)
	face, bounding_box = face_detection(training_image)
	faces.append(face)
	labels.append(label)        

	print ('Training Done')
	return faces, labels

faces, labels = prepare_data('dataset')

model = cv.face.createLBPHFaceRecognizer()
model.train(faces, np.array(labels))
