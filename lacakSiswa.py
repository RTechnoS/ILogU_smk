import fungsi
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

d = fungsi.dB
c = fungsi.c

class lacak:
	def __init__(self, nama):
		namaKorban = 'karim'
		self.logKorban = []
		self.logTerdekat = []
		self.col = ['id', 'Nama', 'Tanggal', 'Waktu', 'Lokasi', 'Terdekat', 'Coor']
		self.logTeman = []