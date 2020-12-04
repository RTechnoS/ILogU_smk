import fungsi, time
import tkinter as tk
from pandas import DataFrame
import matplotlib.pyplot as plt
dB = fungsi.dB
c = fungsi.c

class Main:
	logKorban = []
	logTeman = []
	logTerdekat = {}
	print('import')

	def __init__(self, dash):
		self.dash = dash
		self.namaKorban = tk.StringVar()
		self.namaKorban.set('udin')
		
		self.formData()
		

	def formData(self):
		self.frmDaftar = tk.Toplevel(self.dash)
		self.frmDaftar.geometry('350x200')

		self.frmDaftar.resizable(False, False)
		self.frmDaftar.title('Pelacak')

		tk.Label(self.frmDaftar, text='Nama : ').grid(row=0,column=1)
		inNama = tk.Entry(self.frmDaftar, textvariable=self.namaKorban).grid(row=0, column=2)
		tk.Button(self.frmDaftar, text='Cari', width=10, command=self.winLacak).grid(row=0, column=4, padx=15)
		self.frmDaftar.mainloop()

	def winLacak(self):
		self.frmDaftar.destroy()
		print('Melacak')
		self.__frmLog = tk.Toplevel(self.dash, bg='red')
		self.__frmLog.geometry('500x500')
		self.logWin()
		self.__frmLog.mainloop()

	def logWin(self):
		import lacakSiswa as lck
		dd = lck.lacak(self.namaKorban.get())
		dd.showPlt()
