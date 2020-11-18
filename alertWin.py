import tkinter as tk
import fungsi

class Main:
	def __init__(self):
		self.c = fungsi.c
		self.win = tk.Tk()
		self.win.geometry('800x550')
		self.win.resizable(False, False)
		self.win.title('Pelacak')

		self.namaKorban = tk.StringVar()
		self.namaKorban.set('Nama Siswa')

		__frmData = tk.Frame(self.win)
		__frmData.pack(side=tk.TOP, fill=tk.X, padx=50, pady=30)
		__lblNama = tk.Label(__frmData, text='Nama : ').grid(row=0,column=1)
		inNama = tk.Entry(__frmData, textvariable=self.namaKorban).grid(row=0, column=2)

		

		self.win.mainloop()