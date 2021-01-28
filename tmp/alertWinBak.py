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
		#self.__frmLog.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=15)
		#tunggu.pack()
		self.logWin()
		self.__frmLog.mainloop()

	def logWin(self):
		__sql = 'SELECT * from logSiswa where nama=%s ORDER BY waktu ASC'
		__d = (self.namaKorban.get(),)
		#print(self.namaKorban.get())
		c.execute(__sql,__d)
		__isData = c.fetchall()
		Main.logKorban = __isData
		#print(Main.logKorban)
		self.periksaTeman()
	
	def periksaTeman(self):
		col = ('id', 'Nama', 'Tanggal', 'Waktu', 'Lokasi', 'Terdekat', 'Coor')
		logTerdekat = []
		for log in Main.logKorban:
			idLog ,nama, tanggal, waktu, lokasi, terdekat, coor = log
			#print(str(waktu))
			__sql = "SELECT * from logSiswa where nama!='{}' and tanggal='{}' and lokasi='{}' and waktu like '%{}%' ORDER BY waktu ASC".format(self.namaKorban.get() ,tanggal,lokasi,':'.join(str(waktu).split(':')[0:-1]))
			#print("SELECT * from logSiswa where tanggal={} and lokasi={} and waktu like '%{}%' ORDER BY waktu ASC".format(tanggal,lokasi,':'.join(str(waktu).split(':')[0:-1])))
			c.execute(__sql)
			if log[5] != '' and log[5] != None:
				getTerdekat = log[5]
				for i in getTerdekat.split(','):
					logTerdekat.append(i)

			#print(getTerdekat)
			dataTeman = c.fetchall()
			if len(dataTeman) != 0:
				Main.logTeman.append(dataTeman[0])

		
				#Main.logTerdekat.append()
		#print(Main.logTerdekat)
		#logTerdekat = DataFrame(Main.logTerdekat.value_counts(), columns)
				
		
		dataLog = DataFrame(Main.logTeman, columns=col)
		logNear = list(set(logTerdekat))
		for nameLog in logNear:
			Main.logTerdekat[nameLog] = logTerdekat.count(nameLog)
			#print('Nama : ', nameLog, ' Jumlah : ',logTerdekat.count(nameLog))
		print(list(Main.logTerdekat.values()), list(Main.logTerdekat.keys()))
		#dataLog = 
		#print(dataLog.Terdekat.split(','))
		#print(dataLog.Terdekat.value_counts())
		t = (dataLog.Nama.value_counts())
		#print(dir(t))
		namaOrg = t.keys()
		jumlahLog = t.values
		plt.figure(figsize=(7,5))

		fig, ax = plt.subplots()

		#fig.suptitle('Vertically stacked subplots')
		# axs[0].plot(x, y)
		# axs[1].plot(x, -y)
		# ax = plt.subplot(111)
		# fig, ax = plt.subplots()
		# rects1 = ax.bar(namaOrg, jumlahLog, width=0.3, align='center', color='blue', label='testing bro')
		# rects2 = ax.bar(Main.logTerdekat.keys(), Main.logTerdekat.values(), width=0.3, align='center', color='red')

		def autolabel(rects):
		    """Attach a text label above each bar in *rects*, displaying its height."""
		    for rect in rects:
		        height = rect.get_height()
		        ax.annotate('{}'.format(height),
		                    xy=(rect.get_x() + rect.get_width() / 2, height),
		                    xytext=(0, 3),  # 3 points vertical offset
		                    textcoords="offset points",
		                    ha='center', va='bottom')

		plt1 = ax.bar(namaOrg, jumlahLog, width=0.3, align='center', color='blue', label='testing bro')

		plt2 = ax.bar(Main.logTerdekat.keys(), Main.logTerdekat.values(), width=0.3, align='center', color='red')
		autolabel(plt1)
		autolabel(plt2)
		#plt.xticks()
		plt.show()
		print('Yang pernah bertemu', dataLog.Nama.unique())
		print(dataLog.Nama.value_counts())
				#print(dataLog.Nama.value_counts())
				#nama = []
				#for dttmn in Main.logTeman:

				# 	#logTeman 
				# 	nama.append(dttmn[1])
				# print(nama)

				#print(idLog ,nama, tanggal, waktu, lokasi, terdekat, coor)






