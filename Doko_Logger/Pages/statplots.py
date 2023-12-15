import tkinter as tk
from tkinter import ttk
import tkcalendar as tkc
from datetime import datetime as dt

from Statistik.statistik import Statistiken


LARGEFONT =("Verdana", 30)

class Statplots(tk.Frame):
	def __init__(self, parent, controller): 
		tk.Frame.__init__(self, parent)
		self.controller = controller
		# label of frame Layout 2
		label = ttk.Label(self, text ="DoKo Spieletracker\n",font = LARGEFONT)
		label.grid(row = 0, column = 0, padx = 10, pady = 10, columnspan= 6)
		
		self.Stats = Statistiken

		# Zeitspanne wählen
		self.start_date = tkc.DateEntry(self, date_pattern='dd-MM-yyyy')  
		self.start_date.grid(row = 1, column = 1, padx = 10, pady = 10, columnspan= 1)
		self.start_date.set_date(dt(1990,1,1))
		l1 = ttk.Label(self, text="Von:")
		l1.grid(row = 1, column = 0, padx = 10, pady = 10, sticky=tk.E)

		self.end_date = tkc.DateEntry(self, date_pattern='dd-MM-yyyy')  
		self.end_date.grid(row = 2, column = 1, padx = 10, pady = 10, columnspan= 1)
		l2 = ttk.Label(self, text="Bis:")
		l2.grid(row = 2, column = 0, padx = 10, pady = 10, sticky=tk.E)

		load = ttk.Button(self, text = "Load", command=self.load)
		load.grid(row = 3, column = 1, padx = 10, pady = 10, columnspan=1)

		# Stat Buttons
		self.stat_buttons = [ttk.Button(self, text="Punkte", state= 'disabled', command = lambda : self.Stats.PunktePlot()),
				  ttk.Button(self, text="Soli", state= 'disabled', command = lambda : self.Stats.SoliPlot()),
				  ttk.Button(self, text="Soli wins", state= 'disabled', command = lambda : self.Stats.SoliGewonnenPlot()),
				  ttk.Button(self, text="Runden", state= 'disabled', command = lambda : self.Stats.RundenPlot()),
				  ttk.Button(self, text="Best", state= 'disabled', command = lambda : self.Stats.BestesSpielPlot()),
				  ttk.Button(self, text="Worst", state= 'disabled', command = lambda : self.Stats.SchlechtestesSpielPlot())]
		
		for i in range(len(self.stat_buttons)):
			self.stat_buttons[i].grid(row = i+1, column = 2, padx = 10, pady = 10, columnspan= 2)

		# Back
		self.back = ttk.Button(self, text ="Zurück", command = lambda : self.controller.show_frame(self.controller.pages[0]))
		self.back.grid(row = 4, column = 0, padx = 10, pady = 10)


	def load(self):
		self.Stats = Statistiken(self.controller.Session_Folder_Path, self.start_date.get_date(), self.end_date.get_date())
		
		for button in self.stat_buttons:
			button.state(["!disabled"])
		


		
