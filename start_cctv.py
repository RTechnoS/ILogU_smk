import threading
import video_from_cctv as cctv
import fungsi

#cctv.Cctv(1).Mulai()
class Manager:
	def cekDb():
		#print('sini')
		c = fungsi.dB.cursor()
		__sql = "SELECT * from camera"
		c.execute(__sql)
		isData = c.fetchall()
		return isData

	def startAll():
		for i in Manager.cekDb():
			print(i)
			h = cctv.Cctv(i)
			t = threading.Thread(target=h.Mulai)
			t.start()

	def stopCctv():
		for i in cctv.Cctv.AllFrame.keys():
			h = cctv.Cctv(Manager.cekDb()[i-1])
			h.stopCctv()

	def showCctv():
		print(cctv.Cctv.AllFrame.keys())
		for i in cctv.Cctv.AllFrame.keys():
			#print(Manager.cekDb()[i-1])
			h = cctv.Cctv(Manager.cekDb()[i-1])
			t = threading.Thread(target=h.showFrame)
			t.start()

if __name__ == "__main__":
	startAll()


