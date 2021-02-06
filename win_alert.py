import fungsi, time
import tkinter as tk
from tkinter import ttk

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
		tk.Button(self.frmDaftar, text='Cari', width=10, command=self.selectSiswa).grid(row=0, column=4, padx=15)
		self.frmDaftar.mainloop()


	def selectSiswa(self):
		self.frmDaftar.destroy()
		self.listKorban = tk.Toplevel(self.dash)

		__cek = "SELECT * FROM dataSiswa WHERE nama LIKE '%{}%'".format(self.namaKorban.get())
		c.execute(__cek)
		_isiData = c.fetchall()
		if len(_isiData) >= 1:
			style = ttk.Style(self.listKorban)
			style.configure('Treeview', rowheight=25, height=50)

			self.dataView = ttk.Treeview(self.listKorban)
			self.dataView.grid(row=0, column=1,columnspan=2)
			self.dataView.config(columns=('no', 'nama', 'kelas'), show = "headings")
			
			for t1,t2,t3 in zip(('no', 'nama', 'kelas'),('No', 'Nama', 'Kelas'), (30, 175, 120)):
				self.dataView.heading(t1, text=t2)
				self.dataView.column(t1, width=t3)

			for num, data in enumerate(_isiData):
				self.dataView.insert('','end', values=data)

			scrollData = ttk.Scrollbar(self.listKorban, orient="vertical", command=self.dataView.yview)
			scrollData.grid(row=0, column=3,sticky=tk.N+tk.S)
			self.dataView.configure(yscrollcommand=scrollData.set)
			self.dataView.bind("<Double-1>", self.winLacak)
		else:
			tk.Label(self.listKorban, text='Siswa Tidak Ditemukan', padx=20, pady=20,  fg='red', font=('calibri', 15)).pack()
			
	def winLacak(self, event):

		p = self.dataView.item(self.dataView.selection()[0])
		self.listKorban.destroy()
		self.namaKorban = p['values'][1]
		self.__frmLog = tk.Toplevel(self.dash)
		self.__frmLog.geometry('500x500')
		self.logWin()
		self.__frmLog.mainloop()

	def logWin(self):
		import fungsi_extrak
		
		self.korban = self.namaKorban
		dd = fungsi_extrak.lacak(self.namaKorban)
		self.logKorban = dd.ambilKorban()
		print(dd)
		self.aturData()
		self.showPlt()


	def aturData(self):
		from pandas import read_csv
		self.dataF = read_csv(f"siswa_csv/{self.korban}.csv")
		self.dataF = self.dataF.set_index('nama')
		self.forPlot = self.dataF.sort_values(by=['near', 'oneLoc'])
		if len(self.dataF) >= 15:
			self.forPlot = self.forPlot.head(15)

	def showData(self):
		indexData = list(self.logKorban.keys())
		self.frameList = tk.Frame(self.__frmLog, bg='black')
		self.frameList.pack(side=tk.BOTTOM)

		style = ttk.Style(self.frameList)
		style.configure('Treeview', rowheight=25, height=100)

		self.dataView = ttk.Treeview(self.frameList,selectmode='browse')
		self.dataView.grid(row=0, column=1,columnspan=2)
		self.dataView.config(columns=indexData,show = "headings")

		for t1,t2,t3 in zip(indexData, ('Nama', 'Tanggal', 'Waktu', 'Lokasi', 'Terdekat', 'Koordinat'), (160, 100, 100, 100, 120, 180)):
			self.dataView.heading(t1, text=t2)
			self.dataView.column(t1, width=t3)

		self.isiDataList()

		scrollData = ttk.Scrollbar(self.frameList, orient="vertical", command=self.dataView.yview)
		scrollData.grid(row=0, column=3,sticky=tk.N+tk.S)
		self.dataView.configure(yscrollcommand=scrollData.set)

	def isiDataList(self):
		isData = self.logKorban.values.tolist()
		for i in self.dataView.get_children():
			self.dataView.detach(i)

		for num, data in enumerate(isData):
			self.dataView.insert('','end', values=data)

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
		self.showData()

