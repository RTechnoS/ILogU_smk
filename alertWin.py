import tkinter as tk
import fungsi

class Main:
	def __init__(self, dash):
		self.dash = dash
		self.c = fungsi.c
		self.namaKorban = tk.StringVar()
		self.namaKorban.set('Nama Siswa')

		self.posisi = tk.StringVar()
		self.posisi.set('Loading')
		
		self.formData()
		

	def formData(self):
		self.frmDaftar = tk.Toplevel(self.dash)
		self.frmDaftar.geometry('350x200')

		self.frmDaftar.resizable(False, False)
		self.frmDaftar.title('Pelacak')

		tk.Label(self.frmDaftar, text='Nama : ').grid(row=0,column=1)
		inNama = tk.Entry(self.frmDaftar, textvariable=self.namaKorban).grid(row=0, column=2)
		goBtn = tk.Button(self.frmDaftar, text='Cari', width=10, command=self.lacakLog).grid(row=0, column=4, padx=15)
		self.frmDaftar.mainloop()

	def lacakLog(self):
		self.frmDaftar.destroy()
		print('Melacak')
		self.__frmLog = tk.Toplevel(self.dash, bg='red')
		self.__frmLog.geometry('500x500')
		#self.__frmLog.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=15)

		tunggu = tk.Label(self.__frmLog, text=self.posisi.get()).pack()
		self.__frmLog.mainloop()
