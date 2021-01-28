import fungsi

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
		return self.logKorban

	def prosesData(self):
		self.dataF = pd.DataFrame(columns=('nama', 'oneLoc', 'near', 'hari', 'jumlahHari'))
		self.logKorban = pd.DataFrame(self.logKorban, columns=self.col) # log si korban covid
		self.logTeman = pd.DataFrame(self.logTeman, columns=self.col) # log teman yang pernah satu lokasi dengan korban
		self.logKorban.drop('id',axis=1, inplace=True) 
		self.logTeman.drop('id',axis=1, inplace=True)

		for g in set(self.logTeman.Nama.unique()):
			self.dataF = self.dataF.append({'nama':g, 'near':self.logTerdekat.count(g), 'hari':list(self.logTeman.Tanggal[self.logTeman['Nama'] == g].unique()), 'jumlahHari':len(self.logTeman.Tanggal[self.logTeman['Nama'] == g].unique())} , ignore_index=True)
		tanggalKorban = self.logKorban.sort_values(by='Tanggal').Tanggal.unique() # semua tanggal saat korban terlacak
		
		d = list()
		for tgl in tanggalKorban:
			Lok = self.logTeman[self.logTeman.Tanggal == tgl].Lokasi.unique() #semua tempat(unik) yang delalui korban ex=2020-04-25
			for lk in Lok: #
				for p in self.logTeman[self.logTeman.Tanggal == tgl].sort_values(by='Waktu')['Nama'].unique():
					d.append(p)

		self.dataF = self.dataF.set_index('nama')
		for na in self.dataF.index:
			self.dataF.at[na, 'oneLoc'] = d.count(na)
		self.dataF.to_csv(f'siswa_csv/{self.namaKorban}.csv', index = True)



