import tkinter as tk

from Pages.menu import Menu
from Pages.players import Players
from Pages.gamelog import Gamelog
from Pages.statplots import Statplots

from SessionHandler.session import Session

LARGEFONT =("Verdana", 35)
Session_Folder = "Test_Sessions"
Session_Folder_Path = ".\\"+Session_Folder

class tkinterApp(tk.Tk):
	
	# __init__ function for class tkinterApp 
	def __init__(self, *args, **kwargs): 
		#self.Graph = Graph

		
		#MEIN KRAM
		self.Session_Folder_Path = Session_Folder_Path
		self.session = Session('temp', self.Session_Folder_Path)
		#self.session.new_session(["A","B","C","D","E"], force=True)

		# __init__ function for class Tk
		tk.Tk.__init__(self, *args, **kwargs)
		
		# creating a container
		container = tk.Frame(self) 
		container.pack(side = "top", fill = "both", expand = True) 

		container.grid_rowconfigure(0, weight = 1)
		container.grid_columnconfigure(0, weight = 1)
		

		self.container = container

		# initializing frames to an empty array
		self.pages = [Menu, Players, Gamelog, Statplots]
		self.frames = {} 

		# iterating through a tuple consisting
		# of the different page layouts
		for F in self.pages[0:2]:

			frame = F(container, self)

			# initializing frame of that object from
			# startpage, page1, page2 respectively with 
			# for loop
			self.frames[F] = frame 

			frame.grid(row = 0, column = 0, sticky ="nsew")

		self.show_frame(self.pages[0])

	# to display the current frame passed as
	# parameter
	def show_frame(self, cont):
		try:
			frame = self.frames[cont]
			frame.tkraise()
		except:
			try: 
				self.build_frame(cont)
			except:
				pass
	
	def build_frame(self, cont):
		page = self.pages.index(cont)
		
		frame = cont(self.container, self)
		self.frames[page] = frame 
		frame.grid(row = 0, column = 0, sticky ="nsew")
		
		

#check for "Sessions" Folder, if not existent, create one
import os
path = Session_Folder
# Check whether the specified path exists or not
isExist = os.path.exists(path)
if not isExist:

   # Create a new directory because it does not exist
   os.makedirs(path)
   print("The new directory is created!")
else: 
	print("The directory is existent!")



# Driver Code
app = tkinterApp()
app.mainloop()
