import tkinter as tk
import fungsi, time
import pandas as pd

dB = fungsi.dB
c = fungsi.c

class Main:
	logKorban = []
	logTeman = []
	def __init__(self, dash):
		self.dash = dash
		self.c = fungsi.c
		self.namaKorban = tk.StringVar()
		self.namaKorban.set('Rusman')
		
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
		#self.__frmLog.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=15)
		#tunggu.pack()
		self.logWin()
		self.__frmLog.mainloop()

	def logWin(self):
		__sql = 'SELECT * from logSiswa where nama=%s ORDER BY waktu ASC'
		__d = (self.namaKorban.get(),)
		print(self.namaKorban.get())
		c.execute(__sql,__d)
		__isData = c.fetchall()
		Main.logKorban = __isData
		#print(Main.logKorban)
		self.periksaTeman()
	
	def periksaTeman(self):
		col = ['id', 'Nama', 'Tanggal', 'Waktu', 'Lokasi', 'Terdekat', 'Coor']
		for log in Main.logKorban:
			idLog ,nama, tanggal, waktu, lokasi, terdekat, coor = log
			#print(str(waktu))
			__sql = "SELECT * from logSiswa where nama!='{}' and tanggal='{}' and lokasi='{}' and waktu like '%{}%' ORDER BY waktu ASC".format(self.namaKorban.get() ,tanggal,lokasi,':'.join(str(waktu).split(':')[0:-1]))
			#print("SELECT * from logSiswa where tanggal={} and lokasi={} and waktu like '%{}%' ORDER BY waktu ASC".format(tanggal,lokasi,':'.join(str(waktu).split(':')[0:-1])))
			c.execute(__sql)
			dataTeman = c.fetchall()
			if len(dataTeman) != 0:
				Main.logTeman.append(dataTeman[0])
				
		
		dataLog = pd.DataFrame(Main.logTeman, columns=col)
		print(dataLog)
		print('Yang pernah bertemu', dataLog.Nama.unique())
		print(dataLog.Nama.value_counts())
				#print(dataLog.Nama.value_counts())
				#nama = []
				#for dttmn in Main.logTeman:

				# 	#logTeman 
				# 	nama.append(dttmn[1])
				# print(nama)

				#print(idLog ,nama, tanggal, waktu, lokasi, terdekat, coor)






