import tkinter as tk
from pengambilan_gambar import Mulai as ambilGam
import fungsi, alertWin
import start_cctv as Scctv
import view_data as winData


print(fungsi.getTime('all'))
class Utama:
	pass

class Dashboard(Utama):
	def __init__(self, master):
		self.dash = master
		self.dash.geometry('800x550')
		self.dash.title('Dashboard')
		self.dash.resizable(False, False)

		# self.menubar = tk.Menu(self.dash)

		# fileMenu = tk.Menu(self.menubar, tearoff=0)
		# fileMenu.add_command(label="Exit", command=self.dash.destroy)
		# self.menubar.add_cascade(label="File", menu=fileMenu)

		# toolMenu = tk.Menu(self.menubar, tearoff=0)
		# toolMenu.add_command(label="Settings")
		# self.menubar.add_cascade(label="Tool", menu=toolMenu)

		# helpMenu = tk.Menu(self.menubar, tearoff=0)
		# helpMenu.add_command(label="About")
		# self.menubar.add_cascade(label="Help", menu=helpMenu)

		self.frameAwal = tk.Frame(self.dash)
		self.frameAwal.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
		
		tk.Label(self.frameAwal, text='Aplikasi pelacak Covid-19 Sekolah', fg='red', font=('calibri', 20)).pack()

		frameBtn = tk.Frame(self.frameAwal)
		frameBtn.pack(side=tk.BOTTOM, fill=tk.X)
		rekamBtn = tk.Button(frameBtn, text='Rekam Wajah', state=tk.NORMAL, command=self.addWajah).grid(row=0, column=0, padx=15)
		cekBtn = tk.Button(frameBtn, text='Cek Muka', state=tk.NORMAL).grid(row=0, column=1, padx=15)
		logBtn = tk.Button(frameBtn, text='Lihat Log', state=tk.NORMAL, command=self.logSiswa).grid(row=0, column=2, padx=15)
		dataBtn = tk.Button(frameBtn, text='Data Siswa', state=tk.NORMAL, command=self.dataSiswa).grid(row=0, column=3, padx=15)
		alertBtn = tk.Button(frameBtn, text='ALERT !', state=tk.NORMAL, bg='red', fg='white', padx=20, pady=20, command=self.alertWin).grid(row=0, column=4, padx=15)
		cctvMngrBtn = tk.Button(frameBtn, text='CCTV', state=tk.NORMAL, bg='blue', fg='white', padx=20, pady=20, command=self.cctvManager).grid(row=0, column=5, padx=15)
		testBtn = tk.Button(frameBtn, text='Close', state=tk.NORMAL, command=self.testCmd).grid(row=0, column=6, padx=10)
		#self.dash.config(menu=self.menubar)
		self.dash.mainloop()
	
	def alertWin(self):
		alertWin.Main(self.dash)

	def cctvManager(self):
		Scctv.Manager()
		# winCctv = tk.Tk()
		# winCctv.title('Cctv Manager')
		# winCctv.geometry('1080x720')
		# self.statusCctv = tk.StringVar()

		# cctvStartBtn = tk.Button(winCctv, text='Start Cctv', state=tk.NORMAL, bg='blue', fg='white', padx=20, pady=20, command=Scctv.Manager.startAll).grid(row=0, column=1, padx=15)
		# cctvStopBtn = tk.Button(winCctv, text='Stop Cctv', state=tk.NORMAL, bg='red', fg='white', padx=20, pady=20, command=Scctv.Manager.stopCctv).grid(row=0, column=2, padx=15)
		# cctvShowBtn = tk.Button(winCctv, text='Show Cctv', state=tk.NORMAL, bg='red', fg='white', padx=20, pady=20, command=Scctv.Manager.showCctv).grid(row=0, column=3, padx=15)
		#statusLbl = tk.Label(self.frameAwal, textvariable=self.statusCctv).grid(row=0, column=3, padx=15)

	def logSiswa(self):
		winData.logSiswa(self.dash)

	def dataSiswa(self):
		winData.dataSiswa(self.dash)

	def addWajah(self):
		openBro = ambilGam(self.dash)

	def cekAktif(self):
		hasil = fungsi.checkCctv()

	def testCmd(self):
		#exit()
		import random, datetime
		namaFake = ['haikal','maria','zaky','rifat', 'fikri', 'dwi','udin', 'cin', 'geri', 'amanda','dono', 'astri','dany', 'karim', 'fajar', 'saipul', 'putri', 'rizki'] 

		for i in range(1000):
			nama = random.choice(namaFake)
			lks = random.choice(['kantin1', 'xiimm1', 'xiitkj1', 'kantin2', 'lapangan'])
			aks = random.choice(['salaman', 'tos', 'berpelukan'])
			nea = random.choice(namaFake)+','+random.choice(namaFake)
			coo = '12,34,31,22'
			print(nea)
			hari = random.randrange(1,20)

			tgl = f"2020-01-{hari}"

			jam = random.randrange(7,16)
			akhir = random.randrange(1,30)
			detik = random.randrange(1,60)

			jam = datetime.timedelta(hours=jam, minutes=akhir, seconds=detik)
			fungsi.addLog(nama=nama, tanggal=tgl, waktu=str(jam), lokasi=lks, terdekat=nea, coor=coo)
			print(i)

Dashboard(tk.Tk())