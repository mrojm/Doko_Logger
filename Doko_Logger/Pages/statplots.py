import tkinter as tk
from tkinter import ttk
from Datahandling import Session, Stats
import datetime

LARGEFONT =("Verdana", 30)

class Statplots(tk.Frame):
	def __init__(self, parent, controller): 
		tk.Frame.__init__(self, parent)
		self.controller = controller
		# label of frame Layout 2
		label = ttk.Label(self, text ="DoKo Spieletracker\n",font = LARGEFONT)
		label.place(x=10,y=10,width=400,height=54) 

		# Stats
		self.stats = Stats()
		self.stats.all_session_stats()

		# Positionen
		pos_button = ttk.Button(self, text="Positionen", command=self.pos_callback)

	
	def pos_callback(self):
		data = {}
		for Spieler in self.stats.stats.keys():
			session = self.stats.stats[Spieler]["Sessions"]
			#
			#for session.

		
