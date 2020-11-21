import cv2 as cv
import os, fungsi
import tkinter as tk
from tkinter import messagebox
# from PIL import Image, ImageTk
import fungsi

font = cv.FONT_HERSHEY_SIMPLEX
detector = fungsi.faceDetect('haar')

class Mulai:
	def __init__(self, window):
		self.win = window
		self.nama = tk.StringVar()
		self.nama.set('Bang Jago')

		self.kelas = tk.StringVar()
		self.kelas.set('XII TKJ 1')
		self.__mydb = fungsi.dB
		self.c = fungsi.c
		self.awalan()

	def closing_win(self):
		if messagebox.askokcancel("Quit", "Apakah anda ingin keluar ?"):
			self.cap.release()
			cv.destroyAllWindows()

	def awalan(self):
		self.__winDaftar = tk.Toplevel(self.win)
		self.__winDaftar.title('Daftar')
		
		__frmAwl = tk.Frame(self.__winDaftar)
		__frmAwl.grid(row=0, column=0, padx=30, pady=20)

		tk.Label(__frmAwl, text='Nama = ').grid(row=0, column=1)
		tk.Entry(__frmAwl, textvariable=self.nama).grid(row=0, column=2)
		
		tk.Label(__frmAwl, text='Kelas = ').grid(row=1, column=1)
		tk.Entry(__frmAwl, textvariable=self.kelas).grid(row=1, column=2, pady=5)

		tk.Button(__frmAwl, text='Mulai', command=self.startCap).grid(row=2, column=1, pady=20)
		

	def startCap(self):
		self.__winDaftar.destroy()

		#self.cap = cv.VideoCapture('http://192.168.100.242:4747/video')
		self.cap = cv.VideoCapture(0)
		self.jumlahCap = 0
		nama = (self.nama.get()).replace(' ', '_')
		if not os.path.isdir(f'dataset/{nama}'):
			os.mkdir(f'dataset/{nama}')

		while True:
			#waktu = fungsi.getTime('all')
			_, frame = self.cap.read()
			if _ == False:
				continue
			
			frame = cv.flip(frame, 1)
			#frame = cv.resize(frame, (int(frame.shape[1]/2),int(frame.shape[0]/2)))
				
			faces = detector.face_haar(frame)
			#cv.putText(frame, waktu, (10,10), fontFace=cv.FONT_HERSHEY_PLAIN, fontScale=1, color=(0,0,0))

			for (x, y, w, h) in faces:
				imWajah = frame[y:(y+w), x:(x+w)]
				nl =  f'dataset/{nama}/{self.jumlahCap}_{nama}.jpg'
				cv.imwrite(nl, imWajah)
				cv.rectangle(frame, (x,y), (x+w, y+h), color=(57,196,35), thickness=3)
				cv.putText(frame, "capture :"+str(self.jumlahCap),(x, y-25), font, fontScale=1,thickness=1, color=(15,15, 249))
				self.jumlahCap += 1

			cv.imshow('Perekaman', frame)
			#print(self.__winCap.state())

			if self.jumlahCap <= 100:
				if cv.waitKey(20) & 0xFF == ord('q'):
					self.closing_win()

			else:
				__sql = "SELECT * from dataSiswa where nama=%s and kelas=%s"
				__data = (self.nama.get(), self.kelas.get())
				self.c.execute(__sql, __data)
				isData = self.c.fetchall()

				if len(isData) == 0:
					__sqlAdd = 'INSERT INTO dataSiswa (nama, kelas) VALUES (%s,%s)'
					__dataSql = (self.nama.get(), self.kelas.get())
					self.c.execute(__sqlAdd, __dataSql)
					self.__mydb.commit()

				print('Berhasil Disimpan')
				self.cap.release()
				cv.destroyAllWindows()
				messagebox.showinfo('Succes', "Wajah Berhasil ditambahkan")
			

		startImage()

if __name__ == '__main__':
	aa = tk.Tk()
	Mulai(aa)
	aa.mainloop()

cv.destroyAllWindows()