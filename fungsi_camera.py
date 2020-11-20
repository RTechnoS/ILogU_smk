import numpy as np
import pandas as pd
import random

namaFake = ['haikal','maria','zaky','rifat', 'fikri', 'dwi','udin', 'cin', 'geri', 'amanda','dono', 'astri','dany', 'karim', 'fajar', 'saipul', 'putri', 'rizki'] 


class faceRecog:
	def recog(frame):
		nama = random.choice(namaFake)
		return nama

class Jarak:
	def __init__(self, faces):
		self.faces = faces

	def jarakwajah(self, data):
		print('cek jarak')
		dataFace = pd.DataFrame(self.faces, columns=("kiri","atas","kanan","bawah","nama"))

		print(data)
		#data[2] = data[0]+data[2]
		#data[3] = data[1]+data[3]
		x_jarak = 10
		y_jarak = 5 

		near = []

		for b in dataFace[dataFace['nama'] != data[4]].values:
			if ((data[2]+x_jarak >= b[0] and data[2] <= b[2]+x_jarak) or (data[0]-x_jarak <= b[2] and data[0] >= b[0]+x_jarak)) and ((data[1] < b[3] and data[1] >= b[1]+y_jarak) or (data[3] <= b[3]+y_jarak and data[3] > b[1])):
				print(dataFace[dataFace['nama'] == b[4]].nama.values)
				near.append(dataFace[dataFace['nama'] == b[4]].nama.values)
			print(data[4])
			
		return ','.join(near)
			#print('=============\n')
