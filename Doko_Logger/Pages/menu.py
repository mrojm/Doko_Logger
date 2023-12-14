import tkinter as tk
from tkinter import ttk
from Datahandling import Session
import datetime

LARGEFONT =("Verdana", 30)

class Menu(tk.Frame):
	def __init__(self, parent, controller): 
		tk.Frame.__init__(self, parent)
		self.controller = controller
		# label of frame Layout 2
		label = ttk.Label(self, text ="DoKo Spieletracker  \n",font = LARGEFONT)
		label.place(x=10,y=10,width=500,height=54) 
		self.config( width=500 )

		#Session_Name
		self.sessionname_input = ttk.Entry(self, width=10)
		self.sessionname_input.place(x=160,y=100,width=100,height=25)
		label = ttk.Label(self, text="Session Name", anchor=tk.E)
		label.place(x=50,y=100,width=100,height=25)
		datebutton = ttk.Button(self, text="Datum", command= lambda: [self.sessionname_input.delete(0,'end'),self.sessionname_input.insert(tk.END,datetime.datetime.today().strftime(('%Y-%m-%d')))])
		datebutton.place(x=270,y=100,width=100,height=25)

		# new session
		self.new_session = ttk.Button(self, text ="Neue Session \nerstellen", command = self.new_session)
		self.new_session.place(x=70,y=180,width=100,height=50)

		## button to show frame 2 with text layout2
		self.load_session = ttk.Button(self, text ="Alte Session \nladen", command = self.load_session)
		self.load_session.place(x=190,y=180,width=100,height=50)
	
	def new_session(self):
		session_name = self.sessionname_input.get().strip()
		session = Session(session_name, self.controller.Session_Folder)
		if session_name != "" and not session.session_existent():
			self.controller.session = session
			self.controller.show_frame(self.controller.pages[1])
			self.controller.frames[self.controller.pages[1]].take_name()

	def load_session(self):
		session_name = self.sessionname_input.get().strip()
		if session_name != "":
			session = Session(session_name, self.controller.Session_Folder)

			if session.session_existent():
				session.load_session()
				self.controller.session = session

				self.controller.build_frame(self.controller.pages[2])
				self.controller.show_frame(self.controller.pages[2])
	
	#def stats(self):
	#	self.controller.build_frame(self.controller.pages[3])
	#	self.controller.show_frame(self.controller.pages[3])
		
