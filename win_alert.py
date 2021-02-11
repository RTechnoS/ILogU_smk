import fungsi
from datetime import timedelta, datetime
import tkinter as tk
from tkinter import ttk

c = fungsi.c

class Main:
	def __init__(self, dash):
		self.dash = dash
		self.namaKorban = tk.StringVar()
		self.namaKorban.set('rusman')
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

	def showListData(self, window, dataList, scroll=(0,3), size=(25,50)):
		_isiData, column, titleCol, sizeCol = dataList
		sRow, sCol = scroll
		style = ttk.Style(window)
		style.configure('Treeview', rowheight=size[0], height=size[1])

		dataView = ttk.Treeview(window)
		# for i in dataView.get_children():
		# 	dataView.detach(i)

		dataView.config(columns=column, show = "headings")
			
		for t1,t2,t3 in zip(column,titleCol, sizeCol):
			dataView.heading(t1, text=t2)
			dataView.column(t1, width=t3)

		for num, data in enumerate(_isiData):
			dataView.insert('','end', values=data)

		scrollData = ttk.Scrollbar(window, orient="vertical", command=dataView.yview)
		scrollData.grid(row=sRow, column=sCol,sticky=tk.N+tk.S)
		dataView.configure(yscrollcommand=scrollData.set)
		return dataView


	def selectSiswa(self):
		self.frmDaftar.destroy()
		self.listKorban = tk.Toplevel(self.dash)
		c.execute("SELECT * FROM dataSiswa WHERE nama LIKE '%{}%'".format(self.namaKorban.get()))
		_isiData = c.fetchall()

		if len(_isiData) >= 1:
			self.sameName = self.showListData(self.listKorban, (_isiData,('no', 'nama', 'kelas'),('No', 'Nama', 'Kelas'), (30, 175, 120)))
			self.sameName.grid(row=0, column=1,columnspan=2)
			self.sameName.bind("<Double-1>", self.winLacak)
		else:
			tk.Label(self.listKorban, text='Siswa Tidak Ditemukan', padx=20, pady=20,  fg='red', font=('calibri', 15)).pack()
			
	def winLacak(self, event):
		p = self.sameName.item(self.sameName.selection()[0])
		self.listKorban.destroy()

		self.namaKorban = p['values'][1]
		self.__frmLog = tk.Toplevel(self.dash)
		#self.__frmLog.geometry('700x700')
		self.logWin()
		self.__frmLog.mainloop()

	def logWin(self):
		import fungsi_extrak
		
		self.korban = self.namaKorban
		dd = fungsi_extrak.lacak(self.namaKorban)
		self.logKorban, self.logTeman = dd.ambilKorban()
		#print(self.logKorban.Waktu)
		#print(self.logTeman.Waktu)
		#print(dd.ambilKorban())
		self.aturData()
		self.showPlt()


	def aturData(self):
		from pandas import read_csv
		self.dataF = read_csv(f"siswa_csv/{self.korban}.csv")
		self.dataF = self.dataF.set_index('nama')
		self.friendDetail = self.dataF.sort_values(by=['near', 'oneLoc'], ascending=False)
		if len(self.friendDetail) >= 15:
			self.forPlot = self.friendDetail.head(15)
		else:
			self.forPlot = self.friendDetail

	def historyList(self):
		indexData = list(self.logKorban.keys())
		self.frameList = tk.Frame(self.__frmLog, bg='black')
		self.frameList.pack(side=tk.BOTTOM)
		isData = self.logKorban.values.tolist()
		#print(isData)
		self.hisData = self.showListData(self.frameList, (isData, indexData, ('Nama', 'Tanggal', 'Waktu', 'Lokasi', 'Terdekat', 'Koordinat'), (160, 100, 100, 100, 120, 180)))
		self.hisData.grid(row=0, column=1,columnspan=2)
		self.hisData.bind("<Double-1>", self.click_win_historyList)

	def friendList(self):
		indexData = ('nama', 'countlok', 'countnear', 'countday')
		isData = self.friendDetail.drop('hari', axis=1).reset_index().values.tolist()
		hisFriend = self.showListData(self.frameList, (isData, indexData, ('Nama', 'Satu Lokasi', 'Berdekatan', 'Jumlah Hari'), (160, 100, 100, 100)), (0,7))
		hisFriend.grid(row=0, column=5,columnspan=2)

	def dayList(self):
		isData = self.logKorban.Tanggal.unique()
		print(isData)
		self.hisDay = self.showListData(self.frameList, (isData, ('tanggal',), ('Tanggal',), (160,)), (0,10))
		self.hisDay.grid(row=0, column=8,columnspan=2)
		self.hisDay.bind("<Double-1>", self.click_dayList)

	def click_win_historyList(self, event):
		winSameTime = tk.Toplevel(self.dash)
		p = self.hisData.item(self.hisData.selection())
		dataTeman = p['values'][2]
		splittime = dataTeman[-8:-3]

		sameHist = []
		timeData = []
		for teman in self.logTeman.Waktu:
			jam = teman.to_pytimedelta()
			if splittime in str(jam):
				sameHist = self.logTeman[self.logTeman.Waktu == jam].values.tolist()

		for k in sameHist:
			print(k)
			if k not in timeData:
				timeData.append(k)

		sameTime = self.showListData(winSameTime, (timeData,('id','nama','tanggal', 'waktu', 'lokasi', 'coor'),('Nama', 'Tanggal', 'Waktu', 'Lokasi', 'Koordinat'), (160, 100, 100, 100, 120, 180)))
		sameTime.grid(row=0, column=1, columnspan=2)
		winSameTime.mainloop()

	def click_dayList(self, event):
		self.frameDetail = tk.Frame(self.__frmLog, bg='black')
		self.frameDetail.pack(side=tk.TOP)
		self.select_date = self.hisDay.item(self.hisDay.selection())['values'][0]
		timeData = []
		isData = []
		for teman in self.logTeman.Tanggal.unique():
			tgl = teman.strftime('%Y-%m-%d')
			if self.select_date == tgl:
				timeData = self.logTeman[self.logTeman.Tanggal == teman].Waktu.tolist()

		for k in timeData:
			if str(k)[-8:] not in isData:
				isData.append(str(k)[-8:])
		try:
			self.hisTime.master.destroy()
		except:
			pass

		self.hisTime = self.showListData(self.frameDetail, (isData, ('Jam',), ('Jam',), (160,)), (0,10), size=(20,50))
		self.hisTime.grid(row=0, column=1,columnspan=2)
		self.hisTime.bind("<Double-1>", self.click_win_dayList)


	def click_win_dayList(self, event):
		win_dayList = tk.Toplevel(self.dash)
		jam = self.hisTime.item(self.hisTime.selection())['values'][0]
		isData = []
		tglData = []

		for _tgl in self.logTeman.Tanggal.unique():
			tgl = _tgl.strftime('%Y-%m-%d')
			if tgl == self.select_date:
				tglData = self.logTeman[self.logTeman.Tanggal == _tgl]

		print(tglData)
		for _jam in tglData.Waktu:
			#print(dir(_jam))
			_jam = _jam
			if jam in str(_jam):
				isData = tglData[tglData.Waktu == _jam]
		isData = isData.Waktu.unique()
		print(isData)
		his = self.showListData(win_dayList, (isData, ('id','nama','tanggal', 'waktu', 'lokasi', 'coor'),('Nama', 'Tanggal', 'Waktu', 'Lokasi', 'Koordinat'), (160, 100, 100, 100, 120, 180)))
		his.grid(row=0, column=1,columnspan=2)
		
		win_dayList.mainloop()
		

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
		self.historyList()
		self.friendList()
		self.dayList()
		

