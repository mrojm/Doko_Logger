import datetime
import json
from os import path
from points import Points

class Session:
    
    def __init__(self, filename, folder, add_json=True):
        
        #Datendatei name
        #path = ".\\Sessions\\"
        path = ".\\" + folder + "\\"
        if add_json:
            add_json = ".json"
        else:
            add_json = ""
        self.filename = path +''+ filename + add_json

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
        self.Punkte = Points

        #Register Exceptions
        self.register_exceptions()
        
    
    def new_session(self, Spieler, force=False, Datum=datetime.datetime.today().strftime("%m/%d/%Y, %H:%M:%S")):
        
        #Prüfen ob Datei existiert
        if self.session_existent():
            if force:
                with open(self.filename,'w') as file:
                    file.write("")
            else:
                raise(fileError("File existent"))

        #Neues Dict erstellen
        self.data = self.__dict_new_session(Datum, Spieler)

        #JSON erstellen und DICT speichern
        jsonstring= json.dumps(self.data, indent=3)
    
        with open(self.filename,'a') as file:
            file.write(jsonstring)
        
        #Hilfsvariablen füllen
        self.Spieler = Spieler
        self.Spieleranzahl = len(self.Spieler)

        #Punktetracker erstellen
        self.Punkte = Points(self.Spieler)    
    
    def session_existent(self):
        return path.isfile(self.filename)

    def load_session(self):
        #Prüfen ob Datei existiert
        if not self.session_existent():
            raise(fileError("File nonexistent"))

        #DICT aus JSON laden
        with open(self.filename,"r") as file:
            self.data = json.load(file)
        
        #Hilfsvariablen füllen
        self.Spieler = self.data["Session_Info"]["Spieler"]
        self.Spieleranzahl = len(self.Spieler)
        
        #Bockrunden und Punkte füllen
        Spiele = self.data["Spiele"]
        
        self.Punkte = Points(self.Spieler)
        
        
        for Spiel in Spiele:
            Spiel["Bockrunden"] = len(self.Bockrunden)
            self.Punkte.add_entry(Spiel)     

            self.__update_Bockrunden(Spiel["neue_Bockrunden"])
            
        
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
        self.__update_Bockrunden(nBR)
    
    
    def __update_Bockrunden(self, nBr):
        #Bockrunden als queue gespeichert, jeder Eintrag enthält Lebensdauer der Bockrunde
        #Bsp.: [1,3,4] -> 3 Bockrunden

        #Lebensdauer um einen verringern, falls 0-> aus queue entfernen        
        lock = len(self.Bockrunden)
        i = 0
        while(i < lock):
            self.Bockrunden[i] -=1
            if(self.Bockrunden[i] == 0):
                self.Bockrunden.pop(0)
                i -= 1
                lock -=1
            i +=1

        #Neue Bockrunden hinzufügen (Leben so lange, wie Spieler sind)
        for __ in range(nBr):
            self.Bockrunden.append(self.Spieleranzahl)
    
    
    def __dict_Spieleintrag(self, Spiel: int, Spieler:list, Spieltyp, Gewinner:list, Punkte, BR, nBR):
        
        #Prüfen auf richtige Listenlänge
        if len(Spieler)!=4:
            raise(spielerAnzahl("SpielerAnzahl")) 
        if(Spieltyp == self.NORMALSPIEL and len(Gewinner)!=2):
            raise(gewinnerAnzahl("Gewinneranzahl"))  
        if(Spieltyp == self.SOLO and len(Gewinner)==2):
            raise(gewinnerAnzahl("Gewinneranzahl")) 
        if(len(Gewinner)==4):
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

        

    
    
    
    
    
    
