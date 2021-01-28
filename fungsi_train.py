import cv2
import os
import numpy as np
import pickle

class Cnntrain:
    from keras.models import save_model
    from keras.preprocessing.image import ImageDataGenerator
    from keras.models import Sequential
    from keras.layers import Convolution2D, MaxPool2D, Flatten, Dense

    def __init__(self):
        self.path = './'
        self.ambilImg()

    def ambilImg(self):
        pathImg= self.path+'dataset'

        train_datagen = Cnntrain.ImageDataGenerator(
                shear_range=0.1,
                zoom_range=0.1,
                horizontal_flip=True)
        test_datagen = Cnntrain.ImageDataGenerator()
        self.training_set = train_datagen.flow_from_directory(
                pathImg,
                target_size=(64, 64),
                batch_size=35,
                class_mode='categorical')
        self.test_set = test_datagen.flow_from_directory(
                pathImg,
                target_size=(64, 64),
                batch_size=35,
                class_mode='categorical')
        self.test_set.class_indices

        TrainClasses=self.training_set.class_indices
        ResultMap={}
        for faceValue,faceName in zip(TrainClasses.values(),TrainClasses.keys()):
            ResultMap[faceValue]=faceName.replace('_', ' ')


        with open("trainWajah/wajahCnn.pkl", 'wb') as fileWriteStream:
            pickle.dump(ResultMap, fileWriteStream)

        print(ResultMap)
         
        self.OutputNeurons=len(ResultMap)
        print('\n Jumlah Orang: ', self.OutputNeurons)
        self.trainData()


    def trainData(self):
        classifier = Cnntrain.Sequential()
        classifier.add(Cnntrain.Convolution2D(32, kernel_size=(5, 5), strides=(1, 1), input_shape=(64,64,3), activation='relu'))
        classifier.add(Cnntrain.MaxPool2D(pool_size=(2,2)))
        classifier.add(Cnntrain.Convolution2D(64, kernel_size=(5, 5), strides=(1, 1), activation='relu'))
        classifier.add(Cnntrain.MaxPool2D(pool_size=(2,2)))
        classifier.add(Cnntrain.Flatten())
        classifier.add(Cnntrain.Dense(64, activation='relu'))
        classifier.add(Cnntrain.Dense(self.OutputNeurons, activation='softmax'))
        #classifier.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        classifier.compile(loss='categorical_crossentropy', optimizer = 'adam', metrics=["accuracy"])
        classifier.summary()
        ###########################################################
        from time import time
        StartTime=time()
        classifier.fit(
                            self.training_set,
                            steps_per_epoch=50,
                            epochs=30,
                            validation_data=self.test_set,
                            validation_steps=10)
         
        filepath = self.path+'trainWajah/trainingCnn.h5'
        Cnntrain.save_model(classifier, filepath, save_format='h5')
        
        print("###### Total Time Taken: ", round((time()-StartTime)/60), 'Minutes ######')


class Lbphtrain:
    def __init__(self):
        faces,faceID=Lbphtrain.labels_for_training_data('dataset')
        face_recognizer=Lbphtrain.train_classifier(faces,faceID)
        face_recognizer.write('trainWajah/trainingLbph.yml')

    

    def labels_for_training_data(directory):
        faces=[]
        faceID=[]
        faceLbl = {}

        for num,(path,subdirnames,filenames) in enumerate(os.walk(directory)):
            
            for filename in filenames:
                if filename.startswith("."):
                    print("File system")
                    continue
                img_path=os.path.join(path,filename)
                test_img=cv2.imread(img_path)
                if test_img is None:
                    print("Gambar tidak bisa di baca")
                    continue

                gry = cv2.cvtColor(test_img, cv2.COLOR_BGR2GRAY)
                faces.append(gry)
                faceID.append(num)

            if len(path.split("\\")) == 2:
                nama  = (path.split("\\")[-1]).replace('_', ' ')
                faceLbl[num] = nama

        with open('trainWajah/wajahLbph.pkl', 'wb') as tulis:
            pickle.dump(faceLbl, tulis)

        return faces,faceID

    def train_classifier(faces,faceID):
        face_recognizer=cv2.face.LBPHFaceRecognizer_create()
        face_recognizer.train(faces,np.array(faceID))
        return face_recognizer
