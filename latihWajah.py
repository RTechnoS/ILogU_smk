import cv2
import os
import numpy as np
import pickle

def labels_for_training_data(directory):
    faces=[]
    faceID=[]
    faceLbl = {}

    for num,(path,subdirnames,filenames) in enumerate(os.walk(directory)):
        
        for filename in filenames:
            if filename.startswith("."):
                print("File system")#Skipping files that startwith .
                continue

            img_path=os.path.join(path,filename)#fetching image path
            #print("img_path:",img_path)
            #print("id:",num)
            test_img=cv2.imread(img_path)#loading each image one by one
            if test_img is None:
                print("Gambar tidak bisa di baca")
                continue

            gry = cv2.cvtColor(test_img, cv2.COLOR_BGR2GRAY)
            faces.append(gry)
            faceID.append(num)

        if len(path.split("\\")) == 2:
            nama  = (path.split("\\")[-1]).replace('_', ' ')
            faceLbl[num] = nama

    with open('dataWajah.pkl', 'wb') as tulis:
        pickle.dump(faceLbl, tulis)

    return faces,faceID

def train_classifier(faces,faceID):
    face_recognizer=cv2.face.LBPHFaceRecognizer_create()
    face_recognizer.train(faces,np.array(faceID))
    return face_recognizer

def mulai():
    faces,faceID=labels_for_training_data('dataset')
    face_recognizer=train_classifier(faces,faceID)
    face_recognizer.write('trainingData.yml')

if __name__ == '__main__':
    mulai()