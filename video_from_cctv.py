import cv2 as cv
import fungsi
# import os
import fungsi_camera 
import time, random, threading	


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
			print('Ada Error saat membuka kamera')

		if self.cam.isOpened():
			# wCam = int(self.cam.get(cv.CAP_PROP_FRAME_WIDTH))
			# hCam = int(self.cam.get(cv.CAP_PROP_FRAME_HEIGHT))
			# fourcc = cv.VideoWriter_fourcc(*'XVID')
			hari = fungsi.getTime('hari')
			nama = hari+'_'+self.namaCCTV
			self.video_writer = cv.VideoWriter(f"rekaman/{nama}.mkv", cv.VideoWriter_fourcc(*'XVID'), 25, (int(self.cam.get(cv.CAP_PROP_FRAME_WIDTH)), int(self.cam.get(cv.CAP_PROP_FRAME_HEIGHT))))
			Cctv.AllFrame[self.idCam] = [[], True]

			#self.jumlahCap = 0
			print(self.namaCCTV, 'Kamera Mulai')

			self.detector = fungsi.faceDetect('haar', pengenalan=True) 
			self.detector2 = fungsi.faceDetect('dnn', pengenalan=True) # BAKUP
 
			while Cctv.AllFrame[self.idCam][1] == True and self.cam.isOpened():
				#time.sleep(0.05)
				_, Cctv.AllFrame[self.idCam][0] = self.cam.read()
				# if _ == False:
				# 	continue

				#try:
				if 1+1 == 2:
					frame = Cctv.AllFrame[self.idCam][0]
					waktu = fungsi.getTime()
					#frame = cv.resize(frame, (int(frame.shape[1]/2),int(frame.shape[0]/2)))
					frame = cv.resize(Cctv.AllFrame[self.idCam][0], (640,480))


					#cv.putText(frame, waktu, (10,10), fontFace=cv.FONT_HERSHEY_PLAIN, fontScale=1, color=(0,0,0))
					#Cctv.AllFrame[self.idCam][0] = frame
					#print(frame)
					#self.gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
					#nl =  f'dataset/{self.name}/{self.jumlahCap}_{self.name}.jpg'
					#cv.imwrite(nl, frame)
					self.video_writer.write(frame)
					faces = self.detector.face_haar(frame)

					if len(faces) < 1:
						faces = self.detector2.face_dnn(frame)

					if len(faces) > 1:
						jarak = fungsi_camera.Jarak(faces)

					#fces = []
					for (x, y, w, h, wajah) in faces:
						kanan, bawah = (x+w, y+h)

						cv.rectangle(Cctv.AllFrame[self.idCam][0], (x,y), (kanan, bawah), color=(57,196,35), thickness=2)
						#imWajah = frame[y:(y+w), x:(x+w)]
						#t = threading.Thread(target=fungsi.addLog(nama='Rusman', tanggal=hari, waktu=fungsi.getTime('jam'), lokasi=self.name, terdekat='', interaksi='makan'))
							
						#face_frame = frame[y:bawah, x:kanan]
						#wajah = fungsi_camera.faceRecog.recog(face_frame)
						#fces.append([x, y, kanan, bawah, wajah])

						nearby = ""
						if len(faces) > 1:
							nearby = jarak.jarakwajah([x, y, kanan, bawah, wajah])

						fungsi.addLog(nama=wajah, tanggal=hari, waktu=fungsi.getTime('jam'), lokasi=self.name, terdekat=nearby, coor=str([x,y,kanan,bawah]))


						# if len(faces) > 1:
						# 	jarak.jarakwajah([x,y,kanan,bawah, random.choice(namaFake)])
						#t.start()
						#nl =  f'dataset/{nama}/{self.jumlahCap}_{nama}.jpg'
						#cv.imwrite(nl, imWajah)
							
						#cv.putText(frame, wajah,(x, y-25), cv.FONT_HERSHEY_SIMPLEX, fontScale=1,thickness=1, color=(15,15, 249))
					

					#self.jumlahCap += 1

				# except Exception as e:
				# 	print(e)

			print(self.name, ' Terhenti')
			Cctv.AllFrame[self.idCam] = [[], False]

			self.video_writer.release()
			self.cam.release()
			
			cv.destroyAllWindows()

	def stopCctv(self):
		Cctv.AllFrame[self.idCam][1] = False
		cv.destroyAllWindows()

	def showFrame(self):
		# print(self.idCam)
		#print(Cctv.AllFrame[self.idCam][1])

		while Cctv.AllFrame[self.idCam][1]:	
			if Cctv.AllFrame[self.idCam][0] == []:
				print('error')
				Cctv.AllFrame[self.idCam][1] = False
				break

			frame = cv.resize(Cctv.AllFrame[self.idCam][0], (640,480))

			cv.imshow(self.namaCCTV, frame)

			if cv.waitKey(20) & 0xFF == 27:
				break
		cv.destroyAllWindows()

if __name__ == '__main__':
	pass
