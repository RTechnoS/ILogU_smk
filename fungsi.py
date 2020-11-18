import time
import mysql.connector as db
import cv2 as cv
import numpy as np
from datetime import timedelta

def dataB():
	try:
		__mydb = db.connect(
			host='localhost',
			user='root',
			passwd='',
			db='covidtrack'	
		)
		if __mydb.is_connected():
			return __mydb
				
	except:
		print('Ada Masalah pada database')

dB = dataB()
#print(dB)
c = dB.cursor()

# def checkCctv(idCam='all'):
# 	if idCam != 'all':
# 		if idCama in cctv.Cctv.AllFrame:
# 			return f'{idCam} Sedang aktif'
# 		else:
# 			return f'{idCam} Tidak aktif'
		
# 	else:
# 		cek = cctv.Cctv.AllFrame
# 		print(cek.keys())
# 		return cek.keys()
		

def getTime(apa='all'):
	if apa == 'jam':
		data = time.strftime("%H:%M:%S")
	elif apa == 'hari':
		data = time.strftime("%Y-%m-%d")
	else:
		data = time.strftime("%H:%M:%S %d-%m-%Y")

	return data

#def tambahLog():


def addLog(**data):
	now = data['waktu'].split(':')	
	now = timedelta(hours=int(now[0]), minutes=int(now[1]), seconds=int(now[2]))

	__cek = "SELECT * from logSiswa where nama=%s and tanggal=%s and lokasi=%s ORDER BY waktu DESC limit 1"
	__cekData = (data['nama'], data['tanggal'], data['lokasi'])
	c.execute(__cek, __cekData)
	isData = c.fetchall()
	if len(isData)<1:
		print('++++++++++')
		__sqlAdd = 'INSERT INTO logSiswa (nama, tanggal, waktu, lokasi, terdekat, interaksi) VALUES (%s,%s,%s,%s,%s,%s)'
		__dataSql = (data['nama'], data['tanggal'], data['waktu'], data['lokasi'], data['terdekat'], data['interaksi'])
		c.execute(__sqlAdd, __dataSql)
		dB.commit()
	else:
		for i in isData:
			if (now-i[3]).total_seconds() > 5: 
				print('++++++++++')
				__sqlAdd = 'INSERT INTO logSiswa (nama, tanggal, waktu, lokasi, terdekat, interaksi) VALUES (%s,%s,%s,%s,%s,%s)'
				__dataSql = (data['nama'], data['tanggal'], data['waktu'], data['lokasi'], data['terdekat'], data['interaksi'])
				c.execute(__sqlAdd, __dataSql)
				dB.commit()
			else:
				print('==========')
			


class faceDetect:
	def __init__(self, algo='haar'):
		#self.algo = algo

		if algo == 'haar':
			self.model = cv.CascadeClassifier('model/haarcascade_frontalface_default.xml')
		
		elif algo == 'dnn':
			self.model = cv.dnn.readNetFromCaffe('model/bvlc_googlenet.prototxt', 'model/res10_300x300_ssd_iter_140000.caffemodel')
	
		elif algo == 'mtcnn':
			from mtcnn.mtcnn import MTCNN
			self.model = MTCNN()



	def face_haar(self, frame, scale=1.3, minSize=(10,10)):

		muka = []
		gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

		faces = self.model.detectMultiScale(
		    gray,
			scaleFactor = scale,
			minNeighbors=5,
			minSize=minSize,
			flags=cv.CASCADE_SCALE_IMAGE
		)
		for (x,y,w,h) in faces:
			muka += [[x,y,w,h]]
			
		return(muka)

	def face_dnn(self, frame, conf=1.0): #1.65
		muka = []
		h,w = frame.shape[:2]
		blob = cv.dnn.blobFromImage(cv.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
		self.model.setInput(blob)
		detections = self.model.forward()

		for i in range(0, detections.shape[2]):
			confidence = detections[0,0,i,2]
			if (confidence > conf):
				x, y, kanan, bawah = (detections[0,0,i,3:7] * np.array([w,h,w,h])).astype('int')
				muka += [[x, y, kanan-x, bawah-y]]
			#print(confidence)
		return muka

	def face_mtcnn(self, frame):
		muka = []
		faces = self.model.detect_faces(frame)
		for face in faces:
			#print(face['box'])
			x,y,w,h = face['box']
			muka += [[x,y,w,h]]
			
		return muka



