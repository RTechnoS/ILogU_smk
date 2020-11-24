import threading
import video_from_cctv as cctv
import fungsi
import tkinter as tk
#cctv.Cctv(1).Mulai()
class Manager:
	def __init__(self):
		winCctv = tk.Tk()
		winCctv.title('Cctv Manager')
		winCctv.resizable(False, False)
		#winCctv.geometry('500x500')

		self.statusCctv = tk.StringVar()

		tk.Button(winCctv, text='Start Cctv', state=tk.NORMAL, bg='green', fg='white', padx=20, pady=20, command=Manager.startAll).grid(row=0, column=1, padx=15)
		tk.Button(winCctv, text='Stop Cctv', state=tk.NORMAL, bg='red', fg='white', padx=20, pady=20, command=Manager.stopCctv).grid(row=0, column=2, padx=15)
		tk.Button(winCctv, text='Show Cctv', state=tk.NORMAL, bg='blue', fg='white', padx=20, pady=20, command=Manager.showCctv).grid(row=0, column=3, padx=15)
	
	def cekDb():
		#print('sini')
		c = fungsi.c
		c.execute("SELECT * from camera")
		isData = c.fetchall()
		return isData

	def startAll():
		for i in Manager.cekDb():
			idCam = i[0]
			if idCam not in cctv.Cctv.AllFrame or cctv.Cctv.AllFrame[idCam][1] != True:
				print(i)
				h = cctv.Cctv(i)
				t = threading.Thread(target=h.Mulai)
				t.start()
			else:
				print('Camera', idCam, 'sudah aktif')

	def stopCctv():
		for i in cctv.Cctv.AllFrame.keys():
			h = cctv.Cctv(Manager.cekDb()[i-1])
			h.stopCctv()

	def showCctv():
		#print(cctv.Cctv.AllFrame.keys())
		for i in cctv.Cctv.AllFrame.keys():
			#print(Manager.cekDb()[i-1])
			print('sini ', i)
			print(Manager.cekDb())
			h = cctv.Cctv(Manager.cekDb()[i-1])
			
			t = threading.Thread(target=h.showFrame)
			t.start()

if __name__ == "__main__":
	startAll()


