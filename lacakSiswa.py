import fungsi
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

d = fungsi.dB
c = fungsi.c

class lacak:
	def __init__(self, nama):
		self.namaKorban = nama
		self.logKorban = []
		self.logTerdekat = []
		self.col = ['id', 'Nama', 'Tanggal', 'Waktu', 'Lokasi', 'Terdekat', 'Coor']
		self.logTeman = []
		self.ambilKorban()
	
	def ambilKorban(self):
		c.execute("SELECT * from logSiswa where nama='{}' ORDER BY waktu ASC".format(self.namaKorban))
		__isData = c.fetchall()
		self.logKorban = __isData

		for log in self.logKorban:
		    idLog ,nama, tanggal, waktu, lokasi, terdekat, coor = log
		    __sql = "SELECT * from logSiswa where nama!='{}' and tanggal='{}' and lokasi='{}' and waktu like '%{}%' ORDER BY waktu ASC".format(self.namaKorban ,tanggal,lokasi,':'.join(str(waktu).split(':')[0:-1]))
		    c.execute(__sql)

		    if log[5] != '' and log[5] != None:
		        getTerdekat = log[5]
		        for i in getTerdekat.split(','):
		            self.logTerdekat.append(i)
		    dataTeman = c.fetchall()
		    if len(dataTeman) != 0:
		        self.logTeman.append(dataTeman[0])
		self.prosesData()

	def prosesData(self):
		self.dataF = pd.DataFrame(columns=('nama', 'oneLoc', 'near', 'hari'))
		self.logKorban = pd.DataFrame(self.logTeman, columns=self.col) # log si korban covid
		self.logTeman = pd.DataFrame(self.logTeman, columns=self.col) # log teman yang pernah satu lokasi dengan korban
		self.logKorban.drop('id',axis=1, inplace=True) 
		self.logTeman.drop('id',axis=1, inplace=True)

		for g in set(self.logKorban.Nama.unique()):
			self.dataF = self.dataF.append({'nama':g, 'near':self.logTerdekat.count(g),  'hari':list(self.logTeman.Tanggal[self.logTeman['Nama'] == g].unique())} , ignore_index=True)
		print(self.logKorban)
		tanggalKorban = self.logKorban.sort_values(by='Tanggal').Tanggal.unique() # semua tanggal saat korban terlacak
		
		d = list()
		for tgl in tanggalKorban: 
			Lok = self.logKorban[self.logTeman.Tanggal == tgl].Lokasi.unique() #semua tempat(unik) yang delalui korban ex=2020-04-25
			for lk in Lok: #
				#print(tgl, lk)
				jam = self.logKorban[self.logKorban.Lokasi == lk].sort_values(by='Waktu').Waktu
				for p in self.logTeman[self.logTeman.Tanggal == tgl].sort_values(by='Waktu')['Nama'].unique():
					d.append(p)

		self.dataF = self.dataF.set_index('nama')
		for na in self.dataF.index:
		    self.dataF.at[na, 'oneLoc'] = d.count(na)
		print(self.dataF)




	def showPlt(self):
		def autolabel(rects):
			"""Attach a text label above each bar in *rects*, displaying its height."""
			for rect in rects:
				height = rect.get_height()
				ax.annotate('{}'.format(height),
					xy=(rect.get_x() + rect.get_width() / 2, height),
					xytext=(0, 3),  # 3 points vertical offset
					textcoords="offset points",
					ha='center', va='bottom')
		plt.figure(figsize=(20,10))
		n = self.dataF.index
		locA= self.dataF['oneLoc']
		neaR = self.dataF['near']
		bar_width = 0.35
		fig, ax = plt.subplots()
		index = np.arange(len(n))
		pl1 = ax.bar(index, locA, bar_width, color='r',
		                label='Jumlah Satu Lokasi')

		pl2 = ax.bar(index+bar_width, neaR, bar_width, color='b',
		                label='Jumlah Berdekatan')

		ax.set_xlabel('Nama')
		ax.set_ylabel('Berapa Kali')
		ax.set_title('Static interkasi dengan korban')
		ax.set_xticks(index + bar_width / 2)
		ax.set_xticklabels(self.dataF.index)
		ax.legend()
		autolabel(pl1)
		autolabel(pl2)
		# plt.savefig("tes.png")
		plt.show()
