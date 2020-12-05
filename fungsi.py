from time import strftime
from mysql.connector import connect
import cv2 as cv
import numpy as np
from pandas import DataFrame
from datetime import timedelta

namaFake = ['haikal','maria','zaky','rifat', 'fikri', 'dwi','udin', 'cin', 'geri', 'amanda','dono', 'astri','dany', 'karim', 'fajar', 'saipul', 'putri', 'rizki'] 

def dataB():
	# try:
	_conn = connect(
			host='192.168.100.5',
			user='root',
			passwd='Smkn1.Bkl',
			db='covidtrack',
			auth_plugin='mysql_native_password'
		)
	# if mysql_conn.is_connected():
	# 	return mysql_conn
	return _conn
	# except:
	# 	print('Ada Masalah pada database')

dB = dataB()
c = dB.cursor(buffered=True)

def getTime(apa='all'):
	if apa == 'jam':
		data = strftime("%H:%M:%S")
	elif apa == 'hari':
		data = strftime("%Y-%m-%d")
	else:
		data = strftime("%H:%M:%S %d-%m-%Y")

	return data


def addLog(**data):
	
	dBB = dataB()
	cc = dBB.cursor(buffered=True)

	now = data['waktu'].split(':')	
	now = timedelta(hours=int(now[0]), minutes=int(now[1]), seconds=int(now[2]))

	__cek = "SELECT * from logSiswa where nama=%s and tanggal=%s and lokasi=%s ORDER BY waktu DESC limit 1"
	__cekData = (data['nama'], data['tanggal'], data['lokasi'])
	cc.execute(__cek, __cekData)
	isData = cc.fetchone()
	#print(isData)
	if isData == None:
		print('++++++++++')
		__sqlAdd = 'INSERT INTO logSiswa (nama, tanggal, waktu, lokasi, terdekat, coor) VALUES (%s,%s,%s,%s,%s,%s)'
		__dataSql = (data['nama'], data['tanggal'], data['waktu'], data['lokasi'], data['terdekat'], data['coor'])
		cc.execute(__sqlAdd, __dataSql)
		dBB.commit()
	else:
		if (now.total_seconds()-isData[3].total_seconds()) >= 8:
			__sqlAdd = 'INSERT INTO logSiswa (nama, tanggal, waktu, lokasi, terdekat, coor) VALUES (%s,%s,%s,%s,%s,%s)'
			__dataSql = (data['nama'], data['tanggal'], data['waktu'], data['lokasi'], data['terdekat'], data['coor'])
			cc.execute(__sqlAdd, __dataSql)
			dBB.commit()
			print('++++++++++')
		else:
			pass
			#print('==========')
			

class faceDetect:
	def __init__(self, algo='haar', pengenalan=False):
		from pickle import load
		
		self.pengenalan = pengenalan
		if self.pengenalan == 'lbph':
			with open('trainWajah/wajahLbph.pkl', 'rb') as baca:
				self.name = load(baca)
			self.face_recognizer = cv.face.LBPHFaceRecognizer_create()
			self.face_recognizer.read('trainWajah/trainingLbph.yml')

		elif self.pengenalan == 'cnn':
			from keras.models import load_model
			self.mdlFace = load_model('trainWajah/trainingCnn.h5')
			with open('trainWajah/wajahCnn.pkl', 'rb') as baca:
				self.name = load(baca)

		if algo == 'haar':
			self.model = cv.CascadeClassifier('model/haarcascade_frontalface_default.xml')
		
		elif algo == 'dnn':
			self.model = cv.dnn.readNetFromTensorflow('model/opencv_face_detector_uint8.pb', 'model/opencv_face_detector.pbtxt')
			#self.model = cv.dnn.readNetFromCaffe('model/bvlc_googlenet.prototxt', 'model/res10_300x300_ssd_iter_140000.caffemodel')
	
		elif algo == 'mtcnn':
			from mtcnn.mtcnn import MTCNN
			self.model = MTCNN()



	def face_haar(self, frame, scale=1.3, minSize=(4,4)):
		muka = []
		# gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

		faces = self.model.detectMultiScale(
		    cv.cvtColor(frame, cv.COLOR_BGR2GRAY),
			scaleFactor = scale,
			minNeighbors=5,
			minSize=minSize
		)
		for (x,y,w,h) in faces:
			if self.pengenalan:
				wajah = self.recogWajah(frame[y:y+h, x:x+w])
				muka += [[x,y,w,h,wajah]]
			else:
				muka += [[x,y,w,h]]
			
		return(muka)

	def face_dnn(self, frame, conf=0.135):
		muka = []
		h,w = frame.shape[:2]
		blob = cv.dnn.blobFromImage(cv.resize(frame, (300, 300)), conf, (300, 300), [104, 117, 123], False, False)
		self.model.setInput(blob)
		detections = self.model.forward()

		for i in range(detections.shape[2]):
			#confidence = detections[0,0,i,2]
			if (detections[0,0,i,2] > conf):
				x, y, kanan, bawah = (detections[0,0,i,3:7] * np.array([w,h,w,h])).astype('int')

				if self.pengenalan:
					wajah = self.recogWajah(frame[y:bawah, x:kanan])
					muka += [[x, y, kanan-x, bawah-y, wajah]]
				else:
					muka += [[x, y, kanan-x, bawah-y]]	
		return muka

	def face_mtcnn(self, frame):
		muka = []
		faces = self.model.detect_faces(frame)
		for face in faces:
			#print(face['box'])
			x,y,w,h = face['box']

			if self.pengenalan:
				wajah = self.recogWajah(frame[y:y+h, x:x+w])
				muka += [[x,y,w,h,wajah]]
			else:
				muka += [[x,y,w,h]]
			
		return muka

	def recogWajah(self, wajah):
		if 0 not in wajah.shape:
			if self.pengenalan == 'lbph':
					print(wajah.shape)
					wajah = cv.cvtColor(wajah, cv.COLOR_BGR2GRAY)
					label,confidence=self.face_recognizer.predict(wajah)#predicting the label of given image
					if confidence > 50 and confidence < 190:

						predicted_name=self.name[label]
						print(predicted_name, confidence, '%')
						return predicted_name
					else:
						return 'unkown'
				

			elif self.pengenalan == 'cnn':
				im = cv.resize(wajah, (64,64))
				im = im[...,::-1]
				im = np.expand_dims(im,axis=0)
				result=self.mdlFace.predict(im,verbose=0)
				print(self.name[np.argmax(result)])
				return self.name[np.argmax(result)]
		else:
				return 'unkown'


class Jarak:
	def __init__(self, faces):
		self.faces = faces

	def jarakwajah(self, data):
		dataFace = DataFrame(self.faces, columns=("kiri","atas","kanan","bawah","nama"))
	
		x_jarak = 200
		y_jarak = 100 
		print(len(self.faces))

		near = []

		for b in dataFace[dataFace['nama'] != data[4]].values:
			if ((data[2]+x_jarak >= b[0] and data[2] <= b[2]+x_jarak) or (data[0]-x_jarak <= b[2] and data[0] >= b[0]+x_jarak)):
				if ((data[1] < b[3] and data[1] >= b[1]+y_jarak) or (data[3] <= b[3]+y_jarak and data[3] > b[1])):
					near.append(dataFace[dataFace['nama'] == b[4]].nama.values[0])
		if len(near) != 0:
			print(data[4], "Bersama dengan " , (',').join(near))
			return (',').join(near)
				
