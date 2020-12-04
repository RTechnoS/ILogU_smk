import fungsi, time
import tkinter as tk

dB = fungsi.dB
c = fungsi.c

class Main:
	def __init__(self, dash):
		self.dash = dash
		self.namaKorban = tk.StringVar()
		self.namaKorban.set('udin')
		self.formData()
		

	def formData(self):
		self.frmDaftar = tk.Toplevel(self.dash)
		self.frmDaftar.geometry('400x50')

		self.frmDaftar.resizable(False, False)
		self.frmDaftar.title('Pelacak')

		tk.Label(self.frmDaftar, text='Nama : ').grid(row=0,column=1)
		inNama = tk.Entry(self.frmDaftar, textvariable=self.namaKorban).grid(row=0, column=2)
		tk.Button(self.frmDaftar, text='Cari', width=10, command=self.winLacak).grid(row=0, column=4, padx=15)
		self.frmDaftar.mainloop()

	def winLacak(self):
		self.frmDaftar.destroy()
		self.__frmLog = tk.Toplevel(self.dash)
		self.__frmLog.geometry('500x500')
		self.logWin()
		self.__frmLog.mainloop()

	def logWin(self):
		import lacakSiswa as lck

		self.korban = self.namaKorban.get()
		dd = lck.lacak(self.namaKorban.get())

		self.aturData()
		self.showPlt()


	def aturData(self):
		from pandas import read_csv
		self.dataF = read_csv(f"find/{self.korban}.csv")
		self.dataF = self.dataF.set_index('nama')
		self.forPlot = self.dataF.sort_values(by=['near', 'oneLoc'])
		if len(self.dataF) >= 15:
			self.forPlot = self.forPlot.head(15)

	def showPlt(self):
		import matplotlib.pyplot as plt
		from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
		from numpy import arange

		def autolabel(rects):
			for rect in rects:
				height = rect.get_height()
				ax.annotate('{}'.format(height),
					xy=(rect.get_x() + rect.get_width() / 2, height),
					xytext=(0, 2),  # 3 points vertical offset
					textcoords="offset points",
					ha='center', va='bottom')

		plt.figure(figsize=(10,10), dpi=100)
		
		locA, neaR, jlH = (self.forPlot['oneLoc'], self.forPlot['near'], self.forPlot['jumlahHari'])

		bar_width = 0.35
		fig, ax = plt.subplots()
		
		index = arange(len(self.forPlot.index))
		pl1 = ax.bar(index, locA, bar_width, color='r',
		                label='Jumlah Satu Lokasi')

		pl2 = ax.bar(index+bar_width+0.05, neaR, bar_width, color='b',
		                label='Jumlah Berdekatan')

		pl3 = ax.bar(index, jlH, bar_width, color='g',
		                label='Jumlah Hari')

		ax.set_ylabel('Berapa Kali')
		ax.set_title(f'Static interkasi dengan {self.korban}')
		ax.set_xticks(index + bar_width / 2)
		ax.set_xticklabels(self.forPlot.index)
		
		ax.legend()

		autolabel(pl1)
		autolabel(pl2)
		autolabel(pl3)

		canvas = FigureCanvasTkAgg(fig, self.__frmLog)
		canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH)

