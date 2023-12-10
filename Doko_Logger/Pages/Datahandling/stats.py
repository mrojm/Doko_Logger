import os
from pathlib import Path
import csv
import pandas as pd
from Datahandling.session import Session
import json

#from matplotlib import pyplot as plt

class Stats:
    
    def __init__(self) -> None:
        self.stats = {}

    def make_stats(self):
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



def test():
    stats = Stats()
    stats.all_session_stats()
    stats.save_stats("Statistik_Test.json",override=True)
    stats.write_csv('Test.csv')
    print(stats.stats)


