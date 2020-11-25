import random, datetime
import fungsi, threading
namaFake = ['haikal','maria','zaky','rifat', 'fikri', 'dwi','udin', 'cin', 'geri', 'amanda','dono', 'astri','dany', 'karim', 'fajar', 'saipul', 'putri', 'rizki'] 

def tambah():
	for i in range(10000):
		nama = random.choice(namaFake)
		lks = random.choice(['kantin1', 'xiimm1', 'xiitkj1', 'kantin2', 'lapangan'])
		neaa = random.choice(namaFake)+','+random.choice(namaFake)
		nea = random.choice((neaa, '', random.choice(namaFake)))
		coo = '12,34,31,22'
		print(nea)
		hari = random.randrange(1,20)

		tgl = f"2020-01-{hari}"

		jam = random.randrange(7,16)
		akhir = random.randrange(1,30)
		detik = random.randrange(1,60)

		jam = datetime.timedelta(hours=jam, minutes=akhir, seconds=detik)
		fungsi.addLog(nama=nama, tanggal=tgl, waktu=str(jam), lokasi=lks, terdekat=nea, coor=str([detik,akhir,akhir,detik]))
		print(i)

for i in range(2):
	t = threading.Thread(target=tambah)
	t.start()