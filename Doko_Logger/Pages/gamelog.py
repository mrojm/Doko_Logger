import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo

LARGEFONT =("Verdana", 30)

class Gamelog(tk.Frame): 
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text ="Session Log", font = LARGEFONT)
        label.grid(row = 0, column = 0, padx = 10, pady = 10, columnspan=1+controller.session.Spieleranzahl)
        self.controller = controller

        # Spieler Buttons
        #buttons = [ttk.Button(self, text = "", command = lambda : self.button_function(0), state = "disabled"),
        #             ttk.Button(self, text = "", command = lambda : self.button_function(1), state = "disabled"),
        #               ttk.Button(self, text = "", command = lambda : self.button_function(2), state = "disabled"),
        #            ttk.Button(self, text = "", command = lambda : self.button_function(3), state = "disabled"),
        #              ttk.Button(self, text = "", command = lambda : self.button_function(4), state = "disabled"),
        #            ttk.Button(self, text = "", command = lambda : self.button_function(5), state = "disabled"),
        #            ttk.Button(self, text = "", command = lambda : self.button_function(5), state = "disabled")]
        
        #Define Button as String
        self.buttons = []
        self.button_pressed = []

        # Define Radiobuttons
        self.checkboxes = []

        # Spieler
        self.Spieler = controller.session.Spieler

        #Init Buttons
        label_Spieler = ttk.Label(self, text = "Sitzer:")
        label_Spieler.grid(row=1,column=0,columnspan=1,padx = 10, pady = 10, sticky=tk.E)

        label_Gewinner = ttk.Label(self, text = "Gewinner:")
        label_Gewinner.grid(row=2,column=0,columnspan=1,padx = 10, pady = 10, sticky=tk.E)

        self.init_buttons(self.Spieler)

        # Generate Buttons
        
        # Generate Point Input
        vcmd = (controller.register(self.callback))
        #self.pointinput = ttk.Entry(self, validate='all', validatecommand=(vcmd, '%P')) 
        self.pointinput = ttk.Spinbox(self, from_=0, to=100, validate='all', validatecommand=(vcmd, '%P'))
        self.pointinput.grid(row = 3, column = 1, padx = 10, pady = 10, columnspan=2, sticky=tk.W)
        self.pointinput.insert(0,0)
        
        label_Punkte = ttk.Label(self, text = "Punkte\nohne Bock:")
        label_Punkte.grid(row=3,column=0,columnspan=1,padx = 10, pady = 10, sticky=tk.E)


        #Dropdown Menu
        self.clicked = tk.StringVar()
        options = {controller.session.NORMALSPIEL,
                    controller.session.SOLO}
        self.gamemode = ttk.OptionMenu(self, self.clicked, controller.session.NORMALSPIEL , *options, command= self.option_callback)
        self.gamemode.grid(row = 4, column = 1, padx = 10, pady = 10, columnspan=3,  sticky=tk.W)

        label_Spielmodus = ttk.Label(self, text = "Spieltyp:")
        label_Spielmodus.grid(row=4,column=0,columnspan=1,padx = 10, pady = 10, sticky=tk.E)

        # Bockrunden
        #self.bockrundeninput = ttk.Entry(self, validate='all', validatecommand=(vcmd, '%P')) 
        self.bockrundeninput = ttk.Spinbox(self, from_=0, to=100, validate='all', validatecommand=(vcmd, '%P'))
        self.bockrundeninput.grid(row = 5, column = 1, padx = 10, pady = 10, columnspan=3,  sticky=tk.W)
        self.bockrundeninput.insert(0,0)

        label_neueBR = ttk.Label(self, text = "neue\nBockrunden:")
        label_neueBR.grid(row=5,column=0,columnspan=1,padx = 10, pady = 10, sticky=tk.E)

        label_BR = ttk.Label(self, text = "aktuelle\nBockrunden:\n(Liste mit\nRestrunden\npro Bock)")
        label_BR.grid(row=6,column=0,columnspan=1,padx = 10, pady = 10, sticky=tk.E)

        self.BR = tk.StringVar()
        self.label_BR_Zahl = ttk.Label(self, textvariable=self.BR)
        self.label_BR_Zahl.grid(row=6,column=1,columnspan=2,padx = 10, pady = 10, sticky=tk.W)


        #Spiel Eintragen
        self.speichern = ttk.Button(self, text = "Speichern", command = self.speichern)
        self.speichern.grid(row = 7, column = 1, padx = 10, pady = 10, columnspan=2, sticky=tk.W)

        #Eingabe Punkte mit Bock
        self.points_bock = tk.IntVar()
        self.pointinput_bock = ttk.Spinbox(self, textvariable=self.points_bock, from_=0, to=10000, validate='all', validatecommand=(vcmd, '%P'))
        self.pointinput_bock.grid(row = 3, column = 4, padx = 10, pady = 10, columnspan=2,  sticky=tk.W)
        self.points_bock.trace('w',self.punkte_mit_Bock)

        label_Punkte = ttk.Label(self, text = "Alternativ\nmit Bock:")
        label_Punkte.grid(row=3,column=3,columnspan=1,padx = 10, pady = 10, sticky=tk.E)



        # Punkte darstellen
        self.table_columns = (*self.controller.session.Punkte.df_columns,)
        self.tree = ttk.Treeview(self, columns=self.table_columns, show="headings")
        self.init_table()

        # Create a vertical scrollbar
        yscrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=yscrollbar.set)

        # Pack the Treeview and scrollbar
        self.tree.grid(row = 8, column = 0, padx = 10, pady = 10, columnspan=self.controller.session.Spieleranzahl+1)
        yscrollbar.grid(row = 8, column = self.controller.session.Spieleranzahl, padx = 10, pady = 10, sticky=tk.E)
        
        # Back
        self.back = ttk.Button(self, text ="Zurück",
                            command = lambda : self.controller.show_frame(self.controller.pages[0]))
        self.back.grid(row = 7, column = 3, padx = 10, pady = 10, columnspan=2, sticky=tk.W)
        
        # putting the button in its place by 
        # using grid
        #button1.grid(row = 1, column = 1, padx = 10, pady = 10)

    def init_table(self):
        # Define column headings
        for column in self.table_columns:
            self.tree.heading(column, text=column)
            self.tree.column(column, width=50, anchor=tk.CENTER)
        
        #
        self.tree.column(self.table_columns[2], width=70)
        self.tree.column(self.table_columns[-1], width=100)

        # Insert data
        for index, row in self.controller.session.Punkte.df.iterrows():               
            self.tree.insert("", 0, values=(*row.to_list(),))
        
        self.BR.set(str(self.controller.session.Bockrunden))

    def insert_table(self):
        row = self.controller.session.Punkte.df.loc[len(self.controller.session.Punkte.df)-1]
        self.tree.insert("", 0, values=(*row.to_list(),))

    def callback(self, P):
        if str.isdigit(P) or P == "":
            return True
        else:
            return False
    
    def punkte_mit_Bock(self,*args):
        if self.pointinput_bock.get() == "":
            Punkte_mit_Bock = 0
        else:
            Punkte_mit_Bock = int(self.pointinput_bock.get())
        if Punkte_mit_Bock % int(2**len(self.controller.session.Bockrunden)) == 0:
            self.pointinput.set(Punkte_mit_Bock // int(2**len(self.controller.session.Bockrunden)))
        else:
            self.pointinput.set(0)


    def button_function(self, index):
        if len(self.Spieler) == 4:
            return

        if self.button_pressed.count(True) >= len(self.Spieler)-4:
            self.reset_buttons()
            self.reset_radiobuttons()

        self.button_pressed[index] = True
        self.buttons[index].state(["disabled"])
        if self.checkboxes[index].instate(['selected']):
            self.checkboxes[index].invoke()
        self.checkboxes[index].state(["disabled"])

    def init_buttons(self, Spieler):
        for i in range(len(Spieler)):
            def bcmd(index = i):
                self.button_function(index)

            self.buttons.append(ttk.Button(self, text = "", command = bcmd, state = "disabled"))
            self.checkboxes.append(ttk.Checkbutton(self))
            self.checkboxes[i].invoke()
            self.checkboxes[i].invoke()
            
            self.buttons[i].config(text = self.Spieler[i], state="!disabled")
            self.button_pressed.append(False)

            self.buttons[i].grid(row = 1, column = i+1, padx = 10, pady = 10)
            self.checkboxes[i].grid(row = 2, column = i+1, padx = 10, pady = 10)
            
        self.init_active_players()

    def init_active_players(self):
        if self.controller.session.data["Spiele"] == []:
            return

        spieler_letztes_spiel = self.controller.session.data["Spiele"][-1]["Spieler"]
        for i in range(len(self.Spieler)):
            if not self.Spieler[i] in spieler_letztes_spiel:
                self.button_function(i)
        
        self.button_update()



    def reset_buttons(self):
        for i in range(len(self.button_pressed)):
                self.button_pressed[i] = False
                self.buttons[i].state(["!disabled"])
            
    def reset_radiobuttons(self):
        for i in self.checkboxes:
            i.state(['!disabled'])
            if i.instate(['selected']):
                i.invoke()

    def option_callback(self, option):
        self.clicked.set(option)

    def speichern(self):
        try:
            Spieler = []
            Gewinner = []
            for i in range(len(self.buttons)):
                if(not self.button_pressed[i]):
                    Spieler.append(self.Spieler[i])
                if(self.checkboxes[i].instate(["selected"])):
                    Gewinner.append(self.Spieler[i])
            
            Punkte = int(self.pointinput.get())
            Spielmodus = self.clicked.get()
            neue_Bockrunden = int(self.bockrundeninput.get())

            self.controller.session.log_game(Spieler, Spielmodus, Gewinner, Punkte, neue_Bockrunden)
            
            self.info_updaten()
            self.button_update()
            self.clear_inputs()
        except (self.controller.session.bockFehler,
                self.controller.session.punkteFehler,
                self.controller.session.gewinnerAnzahl,
                self.controller.session.spielnummerFehler,
                self.controller.session.spielerAnzahl
                ) as e:
            showinfo("Window", message=str(e))

    def button_update(self):
        state = self.button_pressed.copy()
        self.reset_buttons()
        self.reset_radiobuttons()
        
        for i in range(len(state)-1):
            if state[i]: 
                self.button_function(i+1)
        if state[-1]: 
                self.button_function(0)


    def clear_inputs(self):
        self.pointinput.delete(0,'end')
        self.pointinput.insert(0,0)
        self.pointinput_bock.delete(0,'end')
        self.pointinput_bock.insert(0,0)
        self.bockrundeninput.delete(0,'end')
        self.bockrundeninput.insert(0,0)
        self.clicked.set(self.controller.session.NORMALSPIEL)

    def info_updaten(self):
        #Tabelle updaten
        self.insert_table()
        #Bockrunden anzeigen
        self.BR.set(str(self.controller.session.Bockrunden))

    
        