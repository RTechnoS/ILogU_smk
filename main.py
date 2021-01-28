import tkinter as tk
import fungsi
import start_cctv as Scctv
print(fungsi.getTime('all'))

class Dashboard:
	def __init__(self, master):
		
		self.dash = master
		p1 = tk.PhotoImage(file = 'logo.png')
		master.iconphoto(True, p1)
		self.dash.geometry('800x550')
		
		#self.dash.configure()
		self.dash.title('I Log U')
		self.dash.resizable(False, False)

		self.frameAwal = tk.Frame(self.dash)
		self.frameAwal.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
		
		tk.Label(self.frameAwal, text='Aplikasi pelacak Covid-19 Sekolah',  fg='red', font=('calibri', 20)).pack()

		frameBtn = tk.Frame(self.frameAwal)
		frameBtn.pack(side=tk.BOTTOM, fill=tk.X)
		tk.Button(frameBtn, text='Rekam Wajah', state=tk.NORMAL, command=self.addWajah).grid(row=0, column=0, padx=15)
		tk.Button(frameBtn, text='Latih Wajah', state=tk.NORMAL, command=self.latihWajah).grid(row=0, column=1, padx=15)
		tk.Button(frameBtn, text='Lihat Log', state=tk.NORMAL, command= lambda: self.logData(0)).grid(row=0, column=2, padx=15)
		tk.Button(frameBtn, text='Data Siswa', state=tk.NORMAL, command=lambda: self.logData(1)).grid(row=0, column=3, padx=15)
		tk.Button(frameBtn, text='ALERT !', state=tk.NORMAL, bg='red', fg='white', padx=20, pady=20, command=self.alertWin).grid(row=0, column=4, padx=15)
		tk.Button(frameBtn, text='CCTV', state=tk.NORMAL, bg='blue', fg='white', padx=20, pady=20, command=Scctv.Manager).grid(row=0, column=5, padx=15)
		self.dash.mainloop()
		
	def latihWajah(self):
		from tkinter import ttk
		def tanyaLatih(apa):
			if tk.messagebox.askokcancel("Latih", "Apakah Anda ingin melatih wajah ?"):
				import latihWajah
				print(apa)
				if apa == 'CNN':
					latihWajah.Cnntrain()
				else:
					latihWajah.Lbphtrain()
				tk.messagebox.showinfo('Succes', "Berhasil Melatih")

		__tanya = tk.Toplevel(self.dash)
		pilihan = tk.StringVar(__tanya)
		pilihan.set('CNN')

		cb = ttk.Combobox(__tanya,textvariable = pilihan, values = ('CNN', 'LBPH')).pack()
		tk.Button(__tanya, text='Latih', command=lambda: tanyaLatih(pilihan.get())).pack()
		__tanya.mainloop()


	def alertWin(self):
		import alertWin
		alertWin.Main(self.dash)
	
	def logData(self, apo):
		import view_data as winData
		if apo == 0:
			winData.logSiswa(self.dash)
		else:
			winData.dataSiswa(self.dash)

	def addWajah(self):
		from pengambilan_gambar import Mulai as ambilGam
		openBro = ambilGam(self.dash)

Dashboard(tk.Tk())