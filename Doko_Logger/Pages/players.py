import tkinter as tk
from tkinter import ttk
import tkcalendar as tkc
from dateutil.parser import parse

LARGEFONT =("Verdana", 35)

class Players(tk.Frame):
    
    def __init__(self, parent, controller):
        
        self.controller = controller
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text ="Auswahl Spieler", font = LARGEFONT)
        self.Page2 = controller.pages[2]
        self.config( width=500 )


        self.grid_columnconfigure(0, weight = 1)
        self.grid_columnconfigure(1, weight = 1)
        self.grid_columnconfigure(2, weight = 1)

        #Spieler Ausgabe
                
        self.Spieler = tk.StringVar()
        self.Spieler_Output = tk.Label(self, textvariable=self.Spieler, height=8, width=10)

        self.Spieler_Input = ttk.Entry(self, width=10)
        #self.session_name = ttk.Entry(self, width=10)

        self.enter_Spieler = ttk.Button(self, text ="Enter",
                            command = self.enter_Spieler_callback)
        
        self.start_game = ttk.Button(self, text ="Start",
                            command = self.start)
        self.back = ttk.Button(self, text ="Zurück",
                            command = lambda : [self.Spieler.set(""),self.controller.show_frame(self.controller.pages[0])])


        # DatePicker
        self.date = tkc.DateEntry(self, date_pattern='dd-MM-yyyy')        
        self.from_name = ttk.Button(self, text = "Sessionname", command = self.take_name)

        self.date.grid(row = 1, column = 0, padx = 10, pady = 10, sticky=tk.S)
        self.from_name.grid(row = 2, column = 0, padx = 10, pady = 10, sticky=tk.N)


        #Positions
        label.grid(row = 0, column = 0, padx = 10, pady = 10, columnspan= 3)
        self.Spieler_Output.grid(row = 1, column = 1, padx = 10, pady = 10, rowspan=2)
        self.enter_Spieler.grid(row = 4, column = 1, padx = 10, pady = 10)
        self.Spieler_Input.grid(row = 3, column = 1, padx = 10, pady = 10)
        # self.session_name.grid(row = 2, column = 2, padx = 10, pady = 10)
        self.start_game.grid(row = 4, column = 2, padx = 10, pady = 10)
        self.back.grid(row = 4, column = 0, padx = 10, pady = 10)
    
    def enter_Spieler_callback(self):
        Spielerstring = self.Spieler.get().strip()
        if input != "":
            self.Spieler.set(Spielerstring + "\n" + self.Spieler_Input.get())
            self.Spieler_Input.delete(0,'end')

    def start(self):
            #Spieler auslesen
            Spieler = self.Spieler.get()
            Spieler = Spieler.split("\n")
            
            # Session erstellen und Namen auslesen
            #session = Session(self.session_name.get())
            # Neue Session Starten

            self.controller.session.new_session(Spieler, Datum=self.date.get_date())


            self.controller.build_frame(self.controller.pages[2])
            self.controller.show_frame(self.controller.pages[2])

    def take_name(self):
        try: 
            date = parse(self.controller.session.filename, fuzzy=True)
            self.date.set_date(date)

        except ValueError:
            return