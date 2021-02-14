import tkinter as tk
from fungsi import c
from tkinter import ttk

class Mulai:
	def __init__(self, win):
		self.win = tk.Toplevel(win)
		self.showData()



	def showData(self):
		self.frameList = tk.Frame(self.win, bg='black')
		self.frameList.pack(side=tk.BOTTOM, fill=tk.X)

		style = ttk.Style(self.frameList)
		style.configure('Treeview', rowheight=25, height=100)

		self.dataView = ttk.Treeview(self.frameList,selectmode='browse')
		self.dataView.grid(row=0, column=1,columnspan=2)
		self.dataView.config(columns=self.indexData,show = "headings")

		for t1,t2,t3 in zip(self.indexData, self.textData, self.ukuranList):
			self.dataView.heading(t1, text=t2)
			self.dataView.column(t1, width=t3)

		self.isiDataList()

		scrollData = ttk.Scrollbar(self.frameList, orient="vertical", command=self.dataView.yview)
		scrollData.grid(row=0, column=3,sticky=tk.N+tk.S)
		self.dataView.configure(yscrollcommand=scrollData.set)
		self.dataView.bind("<Double-1>", self.OnDoubleClick)
	
	def OnDoubleClick(self, event):
		#print(event)
		print(self.dataView.item(self.dataView.selection()[0]))

	def isiDataList(self):
		self.updateData()
		for i in self.dataView.get_children():
			self.dataView.detach(i)

		for num, data in enumerate(self.isData):
			self.dataView.insert('','end', values=data)


class logSiswa(Mulai):
	def __init__(self,win):
		self.indexData = ('id','nama','tanggal', 'waktu', 'lokasi', 'terdekat', 'coor')
		self.textData = ('No','Nama','Tanggal', 'Jam', 'Lokasi', 'Terdekat', 'Kordinat')
		self.ukuranList = (30, 175, 125, 140, 150, 180, 150)
		super().__init__(win)
		self.win.title('Log Siswa')

	def updateData(self):
		c.execute("SELECT * from logSiswa ORDER BY tanggal DESC;")
		self.isData = c.fetchall()
		self.countData = c.rowcount

class dataSiswa(Mulai):
	def __init__(self,win):
		self.indexData = ('id','nama','kelas')
		self.textData = ('No','Nama','Kelas')
		self.ukuranList = (30, 175, 125)
		super().__init__(win)
		self.win.title('Data Siswa')

	def updateData(self):
		c.execute("SELECT * from dataSiswa")
		self.isData = c.fetchall()
		self.countData = c.rowcount