import os
from pathlib import Path
import csv
import pandas as pd
from .session import Session
import json

#from matplotlib import pyplot as plt

class Stats:
    
    def __init__(self) -> None:
        self.stats = {}

    def all_session_stats(self):
        self.stats = self.global_stats(files = self.get_files(os.path.join(Path.cwd(),'Sessions')))

    def save_stats(self, filename, override = False):
        if os.path.isfile(filename):
            if override:
                with open(filename,'w') as file:
                    file.write("")
            else:
                raise Exception("file_existent")
        
        with open(filename,'a') as file:
            file.write(json.dumps(self.stats, indent=3))

    def load_stats(self, filename):
        if os.path.isfile(filename):
            with open(filename,'a') as file:
                self.stats=json.load(file)

    def write_csv(self, filename):
        with open(filename, 'w') as file:
            keys = list(self.stats[list(self.stats.keys())[0]]["Global_stats"].keys())
            keys = ["Spieler", *keys]
            w = csv.DictWriter(file, keys, delimiter=";")
            w.writeheader()
            for Spieler in self.stats.keys():
                temp ={"Spieler": Spieler}
                temp = dict(temp, **self.stats[Spieler]["Global_stats"])
                
                w.writerow(temp)


    def global_stats(self, files):
        
        stats = {}
        for file in files:
            session_stats = self.session_stats(file)
            Spieler = session_stats.keys()
            for Spieler in Spieler:
                try:
                    stats[Spieler]["Sessions"].append(session_stats[Spieler])
                except:
                    stats[Spieler]={"Sessions":[],"Global_stats":{}}
                    stats[Spieler]["Sessions"].append(session_stats[Spieler])
        
        global_stats = {}
        for Spieler in stats:
            global_stats[Spieler] = {"Sessions":0,"Session_Siege":0, "Soli":0, "Soli_gewonnen":0, "Punkte":0, "bestes_Spiel": -10000, "schlechtestes_Spiel": 10000}
            for Session in stats[Spieler]["Sessions"]:
                global_stats[Spieler]["Sessions"] += 1
                global_stats[Spieler]["Soli"] += Session["Soli"]
                global_stats[Spieler]["Soli_gewonnen"] += Session["Soli_gewonnen"]
                global_stats[Spieler]["Punkte"] += Session["Punkte"]
                
                if Session["Position"] == 1:
                    global_stats[Spieler]["Session_Siege"] += 1

                # Bestes Spiel / Schlechtestes Spiel
                if Session["bestes_Spiel"] > global_stats[Spieler]["bestes_Spiel"]:
                    global_stats[Spieler]["bestes_Spiel"] = Session["bestes_Spiel"]
                if Session["schlechtestes_Spiel"] < global_stats[Spieler]["schlechtestes_Spiel"]:
                    global_stats[Spieler]["schlechtestes_Spiel"] = Session["schlechtestes_Spiel"]
            
            stats[Spieler]["Global_stats"] = global_stats[Spieler]
        return stats

    def get_files(self, path):
        for file in os.listdir(path):
            if os.path.isfile(os.path.join(path, file)):
                yield file

    def session_stats(self, filename):
        session = Session(filename, add_json=False)
        session.load_session()

        Datum = session.data["Session_Info"]["Datum"]
        Spieler_ = session.Spieler
        endstand = session.Punkte.df.loc[len(session.Punkte.df)-1]

        Positionen = endstand[Spieler_].sort_values(ascending=False).index
        dict_pos={Positionen[0]:1}
        for i in range(1,len(Positionen),1):
            if endstand[Positionen[i]]==endstand[Positionen[i-1]]:
                dict_pos[Positionen[i]]=dict_pos[Positionen[i-1]]
            else:
                dict_pos[Positionen[i]]=i+1

        # Stats erstellen
        stats = {}
        for Spieler in Spieler_:
            
            stats[Spieler] = {"Datum":"",
                              "Runden":0,
                              "Spieler":0,
                              "Punkte":0,
                              "Position":0,
                              "Siege":0, 
                              "Soli":0, 
                              "Soli_gewonnen":0, 
                              "bestes_Spiel": -10000, 
                              "schlechtestes_Spiel": 10000
                              }


            #Session_Info
            stats[Spieler]["Datum"] = Datum
            stats[Spieler]["Runden"] = endstand["Runde"]
            stats[Spieler]["Spieler"]= len(Spieler_)

            #Endstand
            stats[Spieler]["Punkte"] = endstand[Spieler]
            stats[Spieler]["Position"] = dict_pos[Spieler]
            
            #Persönliche Stats
            for game in session.data["Spiele"]:
                Punkte = session.Punkte.calc_points(game)
                if Spieler in game["Spieler"]:

                    # Siege
                    if Spieler in game["Gewinner"]:
                        stats[Spieler]["Siege"] += 1

                    # Soli
                    if game["Spieltyp"] == session.SOLO:
                        if len(game["Gewinner"])==1 and (Spieler in game["Gewinner"]):
                            stats[Spieler]["Soli"] += 1
                            stats[Spieler]["Soli_gewonnen"] += 1
                        elif len(game["Gewinner"])==3 and not (Spieler in game["Gewinner"]):
                            stats[Spieler]["Soli"] += 1
                    
                    # Bestes Spiel / Schlechtestes Spiel
                    if Punkte[Spieler] > stats[Spieler]["bestes_Spiel"]:
                        stats[Spieler]["bestes_Spiel"] = Punkte[Spieler]
                    if Punkte[Spieler] < stats[Spieler]["schlechtestes_Spiel"]:
                        stats[Spieler]["schlechtestes_Spiel"] = Punkte[Spieler]

        return stats


def test():
    stats = Stats()
    stats.all_session_stats()
    stats.save_stats("Statistik_Test.json",override=True)
    stats.write_csv('Test.csv')
    print(stats.stats)


