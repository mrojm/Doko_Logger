import os
from pathlib import Path
import csv
import pandas as pd
from Datahandling.session import Session
import json

#from matplotlib import pyplot as plt

class Stats:
    
    def __init__(self, session_folder_path) -> None:
        self.session_stats = {}
        self.sessions = []
        self.session_folder_path = session_folder_path
        self.global_stats = pd.DataFrame

        self.global_stats_keys = ["Sessions_gespielt",
                              "Sessions_gewonnen",
                              "Runden_gespielt",
                              "Soli_gespielt",
                              "Soli_gewonnen",
                              "Punkte_Total",
                              "bestes_Spiel",
                              "schlechtestes_Spiel"]
        """
        self.session_stats = ["Datum",
                              "Runden",
                              "Spieler",
                              "Punkte",
                              "Position",
                              "Siege",
                              "Soli",
                              "Soli_gewonnen",
                              "bestes_Spiel",
                              "schlechtestes_Spiel"]
        """

        self.__load_sessions(session_folder_path)
        self.make_global_stats()

        
    def __load_sessions(self, session_folder_path):
        # Für jede Session im Ordner

        session_stats_list = {}
        for sessionname in self.__get_sessions(session_folder_path):

            #Ordner Name
            folder = os.path.basename(os.path.normpath(session_folder_path))
            
            #Session erstellen und laden
            session = Session(sessionname, folder, add_json=False)
            session.load_session()
            self.sessions.append(session)

            session_stats = session.session_stats()
            # Spieler laden und Dataframe erstellen
            for Spieler in session_stats:
                #Falls Spieler erstmalig gesehen, neuen Eintrag machen
                if Spieler not in session_stats_list.keys():
                    session_stats_list[Spieler] = []
                
                # Sessionstats ablegen
                session_stats_list[Spieler].append(session_stats[Spieler])

        # Daten ins Objekt laden
        for Spieler in session_stats_list.keys():
            self.session_stats[Spieler] = pd.DataFrame.from_records(session_stats_list[Spieler]).set_index("Datum")

            
    @staticmethod
    def __get_sessions(path):
        for file in os.listdir(path):
            if os.path.isfile(os.path.join(path, file)):
                yield file


    def make_global_stats(self):
        stats = []
        for Spieler in self.session_stats.keys():
            session_stats_P = self.session_stats[Spieler]
            
            global_stats = {}

            # Sessions
            global_stats["Sessions_gespielt"] = len(session_stats_P)

            # Runden
            global_stats["Runden_gespielt"] = session_stats_P["Runden"].sum()

            # Soli
            global_stats["Soli_gespielt"] = session_stats_P["Soli"].sum()
            global_stats["Soli_gewonnen"] = session_stats_P["Soli_gewonnen"].sum()

            # Punkte
            global_stats["Punkte_Total"] = session_stats_P["Punkte"].sum()

            # Session Siege
            global_stats["Sessions_gewonnen"] = session_stats_P['Position'].apply(lambda x: 0 if x != 1 else 1).sum()

            #Bestes Spiel
            global_stats["bestes_Spiel"] = session_stats_P["bestes_Spiel"].max()

            #Bestes Spiel
            global_stats["schlechtestes_Spiel"] = session_stats_P["schlechtestes_Spiel"].min()

            stats.append(global_stats)

        self.global_stats = pd.DataFrame.from_records(stats, index = self.session_stats.keys())
    

    def __old_global_stats(self, sessionnames, filenames_include_json_ending = True):
        
        # Global Stats Dict
        global_stats = {}

        #Alle Sessions durchgehen
        for sessionname in sessionnames:
            
            # Session laden und Statistik abrufen
            session = Session(sessionname, add_json= not filenames_include_json_ending)
            session.load_session()
            session_stats = session.session_stats()

            # Für jeden Spieler eintrag schreiben und updaten
            for Spieler in Spieler:
                #Session Statistik von Spieler
                session_stats_P = session_stats[Spieler]

                # Eintrag erstellen, falls Spieler das erste Mal auftaucht
                if Spieler not in global_stats.keys():
                    global_stats[Spieler]={"Sessions":[],
                                           "Global":{"Sessions_gespielt":0,
                                                     "Sessions_gewonnen":0,
                                                     "Runden_gespielt":0, 
                                                     "Soli_gespielt":0, 
                                                     "Soli_gewonnen":0, 
                                                     "Punkte_Total":0, 
                                                     "bestes_Spiel": -10000, 
                                                     "schlechtestes_Spiel": 10000}}
                    
                # Session_stats in Globalstats eintragen
                global_stats[Spieler]["Sessions"].append(session_stats_P)

                #Globale Statistik mit Sessionstatistik updaten
                global_performance = global_stats[Spieler]["Global"]

                # Zählen
                global_performance["Sessions_gespielt"] += 1
                global_performance["Soli_gespielt"] += session_stats_P["Soli_gespielt"]
                global_performance["Soli_gewonnen"] += session_stats_P["Soli_gewonnen"]
                global_performance["Punkte_Total"] += session_stats_P["Punkte_Total"]

                # Session_Siege
                if session_stats_P["Position"] == 1:
                    global_stats[Spieler]["Sessions_gewonnen"] += 1

                # Bestes Spiel / Schlechtestes Spiel
                if session_stats_P["bestes_Spiel"] > global_performance["bestes_Spiel"]:
                    global_performance["bestes_Spiel"] = session_stats_P["bestes_Spiel"]
                if session_stats_P["schlechtestes_Spiel"] < global_performance["schlechtestes_Spiel"]:
                    global_performance["schlechtestes_Spiel"] = session_stats_P["schlechtestes_Spiel"]

        return global_stats
