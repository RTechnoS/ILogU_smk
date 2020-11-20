import cv2 as cv
import fungsi
# import os
import fungsi_camera 
import time, random

namaFake = ['haikal','maria','zaky','rifat', 'fikri', 'dwi','udin', 'cin', 'geri', 'amanda','dono', 'astri','dany', 'karim', 'fajar', 'saipul', 'putri', 'rizki'] 

class Cctv:
	AllFrame = {}
	def __init__(self, dataCam):
		#print(dataCam)
		#self.dataCam = dataCam
		self.idCam, self.namaCCTV, self.name, self.url = dataCam
		#print(self.url)
		

	def Mulai(self):
		# if not os.path.isdir(f'dataset/{self.name}'):
		# 	os.mkdir(f'dataset/{self.name}')
		try:
			self.cam = cv.VideoCapture(self.url)
		except:
			exit()

		if self.cam.isOpened():
			w = int(self.cam.get(cv.CAP_PROP_FRAME_WIDTH))
			h = int(self.cam.get(cv.CAP_PROP_FRAME_HEIGHT))
			fourcc = cv.VideoWriter_fourcc(*'XVID')
			hari = fungsi.getTime('hari')
			nama = hari+'_'+self.namaCCTV
			self.video_writer = cv.VideoWriter(f"rekaman/{nama}.mkv", fourcc, 25, (w, h))
			Cctv.AllFrame[self.idCam] = {'on':True, 'frame':None}

			self.jumlahCap = 0
			print(self.namaCCTV, 'Kamera Mulai')

			self.detector = fungsi.faceDetect('haar') 
			self.detector2 = fungsi.faceDetect('dnn') # BAKUP
 
			while Cctv.AllFrame[self.idCam]['on'] == True and self.cam.isOpened():
				#time.sleep(0.2)
				_, Cctv.AllFrame[self.idCam]['frame'] = self.cam.read()
				if _ == False:
					continue

				try:
					frame = Cctv.AllFrame[self.idCam]['frame']
					waktu = fungsi.getTime()
					#frame = cv.resize(frame, (int(frame.shape[1]/2),int(frame.shape[0]/2)))
					#frame = cv.resize(frame, (640,480))

					cv.putText(frame, waktu, (10,10), fontFace=cv.FONT_HERSHEY_PLAIN, fontScale=1, color=(0,0,0))
					Cctv.AllFrame[self.idCam]['frame'] =frame
					#print(frame)
					#self.gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
					#nl =  f'dataset/{self.name}/{self.jumlahCap}_{self.name}.jpg'
					#cv.imwrite(nl, frame)
					self.video_writer.write(frame)
					#faces = self.detector.face_dnn(frame, conf=0.14)
					faces =  self.detector2.face_dnn(frame)

					if len(faces) < 1:
						faces = self.detector.face_haar(frame)

					if len(faces) >= 1:
						jarak = fungsi_camera.Jarak(faces)
					#fces = []#fungsi_camera.jarakwajah(faces)
					for (x, y, w, h) in faces:
							#imWajah = frame[y:(y+w), x:(x+w)]
							#t = threading.Thread(target=fungsi.addLog(nama='Rusman', tanggal=hari, waktu=fungsi.getTime('jam'), lokasi=self.name, terdekat='', interaksi='makan'))
							
							fungsi.addLog(nama='Rusman', tanggal=hari, waktu=fungsi.getTime('jam'), lokasi=self.name, terdekat='', interaksi='makan')
							if len(faces) > 1:
								jarak.jarakwajah([x,y,x+w,y+h, random.choice(namaFake)])
							#t.start()
							#nl =  f'dataset/{nama}/{self.jumlahCap}_{nama}.jpg'
							#cv.imwrite(nl, imWajah)
							cv.rectangle(frame, (x,y), (x+w, y+h), color=(57,196,35), thickness=2)
							#cv.putText(frame, "capture :"+str(self.jumlahCap),(x, y-25), font, fontScale=1,thickness=1, color=(15,15, 249))
					
					self.jumlahCap += 1

				except Exception as e:
					print(e)

			print(self.name, ' Terhenti')

			self.video_writer.release()
			self.cam.release()
			
			cv.destroyAllWindows()

	def stopCctv(self):
		Cctv.AllFrame[self.idCam]['on'] = False
		cv.destroyAllWindows()

	def showFrame(self):
		# print(self.idCam)
		#print(Cctv.AllFrame[self.idCam]['on'])
		while Cctv.AllFrame[self.idCam]['on']:
			frame = Cctv.AllFrame[self.idCam]['frame']
			#print(frame)			
			if Cctv.AllFrame[self.idCam]['frame'] == []:
				break

			frame = cv.resize(frame, (640,480))

			cv.imshow(self.namaCCTV, frame)

			if cv.waitKey(20) & 0xFF == 27:
				break

if __name__ == '__main__':
	pass
