import datetime
import json
from os import path
from SessionHandler.pointtracker import PointTracker
from SessionHandler.results import Results as rs

class Session:
    
    def __init__(self, filename, folder, add_json=True):
        
        #Datendatei name
        #path = ".\\Sessions\\"
        path = folder + "\\"
        if add_json:
            add_json = ".json"
        else:
            add_json = ""
        self.filename = path + filename + add_json

        #Dict mit Session_Info und Spieleinträgen
        self.data = {}

        #Hilfsvariablen für schnellen Zugriff
        self.Bockrunden = []
        self.Spieler = []
        self.Spieleranzahl = 0
        
        #Spiel Definitionen
        self.NORMALSPIEL = "NORMALSPIEL"
        self.SOLO = "SOLO"

        # Punktestand
        self.Punkte = PointTracker

        #Register Exceptions
        self.register_exceptions()
        
    
    def new_session(self, Spieler:list, force=False, Datum=datetime.date.today()):
        
        #Prüfen ob Datei existiert
        if self.session_existent():
            if force:
                with open(self.filename,'w') as file:
                    file.write("")
            else:
                raise(fileError("File existent"))
        
        #Prüfen, ob Spielernamen einzigartig sind
        for S in Spieler:
            if Spieler.count(S) > 1:
                raise SpielerNamen("Nutze einzigartige Spielernamen")


        #Neues Dict erstellen
        self.data = self.__dict_new_session(Datum.strftime("%m/%d/%Y"), Spieler)

        #JSON erstellen und DICT speichern
        jsonstring= json.dumps(self.data, indent=3)
    
        with open(self.filename,'a') as file:
            file.write(jsonstring)
        
        #Hilfsvariablen füllen
        self.Spieler = Spieler
        self.Spieleranzahl = len(self.Spieler)

        #Punktetracker erstellen
        self.Punkte = PointTracker(self.Spieler)    
    
    def session_existent(self):
        return path.isfile(self.filename)

    def load_session(self):
        #Prüfen ob Datei existiert
        if not self.session_existent():
            raise(fileError("File nonexistent"))

        #Zustand löschen
        #Dict mit Session_Info und Spieleinträgen
        self.data = {}

        #Hilfsvariablen für schnellen Zugriff
        self.Bockrunden = []
        self.Spieler = []
        self.Spieleranzahl = 0
        
        #DICT aus JSON laden
        with open(self.filename,"r") as file:
            self.data = json.load(file)
        
        #Hilfsvariablen füllen
        self.Spieler = self.data["Session_Info"]["Spieler"]
        self.Spieleranzahl = len(self.Spieler)
        
        #Bockrunden und Punkte füllen
        Spiele = self.data["Spiele"]
        
        self.Punkte = PointTracker(self.Spieler)
        
        
        for Spiel in Spiele:
            Spiel["Bockrunden"] = len(self.Bockrunden)
            self.Punkte.add_entry(Spiel)     

            self.__update_Bockrunden(self.Bockrunden, Spiel["neue_Bockrunden"])
            
        
    def log_game(self, Spieler:list, Spieltyp, Gewinner:list, Punkte, nBR):
        
        #Spielnummer
        Spiele = self.data["Spiele"]
        Spiel = 1
        if Spiele: #List Empty
            Spiel = Spiele[-1]["Spiel"]+1
        
        #aktuelle Bockrunden
        BR = len(self.Bockrunden)
        
        #DICT updaten
        game_dict = self.__dict_Spieleintrag(Spiel, Spieler, Spieltyp, Gewinner, Punkte, BR, nBR)
        self.data["Spiele"].append(game_dict)

        #DICT in JSON schreiben
        jsonstring = json.dumps(self.data, indent=3)
        with open(self.filename,'w') as file:
            file.write(jsonstring)

        #Punkte updaten
        game_dict["Bockrunden"] = BR
        self.Punkte.add_entry(game_dict)

        #aktuelle Bockrunden updaten
        self.__update_Bockrunden(self.Bockrunden, nBR)
    
    def change_game(self, Spielnummer, Spieler:list, Spieltyp, Gewinner:list, Punkte, nBR):
        if len(self.data["Spiele"]) < Spielnummer:
            raise spielnummerFehler("Spiel gibt es nicht")
        
        BR = len(self.Bockrunden)
        #DICT erhalten
        game_dict = self.__dict_Spieleintrag(Spielnummer, Spieler, Spieltyp, Gewinner, Punkte, BR, nBR)

        self.data["Spiele"][Spielnummer-1] = game_dict
        
        #DICT in JSON schreiben
        jsonstring = json.dumps(self.data, indent=3)
        with open(self.filename,'w') as file:
            file.write(jsonstring)
        
        self.load_session()

    def get_game(self, Spielnummer):
        if len(self.data["Spiele"]) < Spielnummer:
            raise spielnummerFehler("Spiel gibt es nicht")
        
        Bockrunden = []
        for Spiel in self.data["Spiele"][:Spielnummer-1]:
            self.__update_Bockrunden(Bockrunden, Spiel["neue_Bockrunden"])
        
        spiel = self.data["Spiele"][Spielnummer-1]
        spiel["Bockrunden"] = Bockrunden

        return spiel

    def Results(self):
        # Returns Session stats as dict
        return rs(self)

    def __update_Bockrunden(self, l_Bockrunden, nBr):
        #Bockrunden als queue gespeichert, jeder Eintrag enthält Lebensdauer der Bockrunde
        #Bsp.: [1,3,4] -> 3 Bockrunden

        #Lebensdauer um einen verringern, falls 0-> aus queue entfernen        
        lock = len(l_Bockrunden)
        i = 0
        while(i < lock):
            l_Bockrunden[i] -=1
            if(l_Bockrunden[i] == 0):
                l_Bockrunden.pop(0)
                i -= 1
                lock -=1
            i +=1

        #Neue Bockrunden hinzufügen (Leben so lange, wie Spieler sind)
        for __ in range(nBr):
            l_Bockrunden.append(self.Spieleranzahl)
    
    
    def __dict_Spieleintrag(self, Spiel: int, Spieler:list, Spieltyp, Gewinner:list, Punkte, BR, nBR):
        
        #Prüfen auf richtige Listenlänge
        if len(Spieler)!=4:
            raise(spielerAnzahl("SpielerAnzahl")) 
        if(Spieltyp == self.NORMALSPIEL and len(Gewinner)!=2):
            raise(gewinnerAnzahl("Gewinneranzahl"))  
        if(Spieltyp == self.SOLO and len(Gewinner)==2):
            raise(gewinnerAnzahl("Gewinneranzahl")) 
        if(len(Gewinner) < 1 or len(Gewinner) > 3):
            raise(gewinnerAnzahl("Gewinneranzahl"))
        if(Punkte<=0):
            raise(punkteFehler("Punktefehler"))
        if(nBR<0):
            raise(bockFehler("Bockfehler"))
        if(BR<0):
            raise(bockFehler("Bockfehler"))
        if(Spiel<=0):
            raise(spielnummerFehler("Spielnummerfehler"))

        #Definition eines Spieleintrags
        entry = {"Spiel": Spiel,
                 "Spieler": Spieler,
                 "Spieltyp": Spieltyp,
                 "Gewinner": Gewinner,
                 "Punkte": Punkte,
                 #"Bockrunden": BR,
                 "neue_Bockrunden": nBR
                }
                
        return entry    
    
    def __dict_new_session(self, Datum, Spieler:list):
        
        if len(Spieler)<4:
            raise(spielerAnzahl("SpielerAnzahl")) 
        
        #Session Struktur, gespeichert in einer JSON
        session_info = {"Datum": Datum, 
                        "Spieler": Spieler,
                        "Endergebnis": {}
                        }
        
        entry = {"Session_Info": session_info,
                 "Spiele": []}

        return entry
    
    def register_exceptions(self):
        self.fileError = fileError
        self.spielerAnzahl = spielerAnzahl
        self.gewinnerAnzahl = gewinnerAnzahl
        self.punkteFehler = punkteFehler
        self.bockFehler = bockFehler
        self.spielnummerFehler = spielnummerFehler

    
class fileError(Exception):
    pass

class spielerAnzahl(Exception):
    pass

class gewinnerAnzahl(Exception):
    pass

class punkteFehler(Exception):
    pass

class bockFehler(Exception):
    pass

class spielnummerFehler(Exception):
    pass

class SpielerNamen(Exception):
    pass
        

    
    
    
    
    
    
