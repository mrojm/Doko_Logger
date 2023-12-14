import os
from pathlib import Path
import csv
import pandas as pd
from Datahandling.session import Session
from datetime import datetime

class Global_stats:
    
    def __init__(self, session_folder_path, start_date = datetime(1990,1,1), end_date = datetime.today()) -> None:
        self.session_stats = None
        self.sessions = []
        self.session_folder_path = session_folder_path
        

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
        #self.global_stats = self.calc_global_stats()

    def get_global_Runden_column(self, Spieler):
        return self.session_stats[Spieler,"Runden"].cumsum()
    
    def get_global_Punkte_column(self,Spieler):
        return self.session_stats[Spieler,"Punkte"].cumsum()
            
    def get_global_Soli_column(self,Spieler):
        return self.session_stats[Spieler,"Soli"].cumsum()
    
    def get_global_Soligewonnen_column(self,Spieler):
        return self.session_stats[Spieler,"Soli_gewonnen"].cumsum()
    
    def get_global_Siege_column(self,Spieler):
        Series = self.session_stats[Spieler,"Position"].apply(lambda x: 0 if x != 1 else 1)
        return Series.cumsum()
       
    def get_global_BestesSpiel_column(self,Spieler):
        return self.session_stats[Spieler,"bestes_Spiel"].cummax()
      
    def get_global_SchlechtestesSpiel_column(self,Spieler):
        return self.session_stats[Spieler,"schlechtestes_Spiel"].cummin()

    def __load_sessions(self, session_folder_path):
        # Für jede Session im Ordner

        session_stats_list = []
        for sessionname in self.__get_sessions(session_folder_path):

            #Ordner Name
            folder = os.path.basename(os.path.normpath(session_folder_path))
            
            #Session erstellen und laden
            session = Session(sessionname, folder, add_json=False)
            session.load_session()
            
            #Check if Session empty
            if len(session.Punkte.df) == 0:
                continue

            self.sessions.append(session)

            session_stats = session.session_stats()
            # Spieler laden und Dataframe erstellen
            for Spieler in session_stats:
                # Sessionstats ablegen
                session_stats[Spieler]["Name"] = Spieler
                session_stats_list.append(session_stats[Spieler])

            self.session_stats = pd.DataFrame.from_records(session_stats_list).set_index(["Name","Datum"])
            

            
    @staticmethod
    def __get_sessions(path):
        for file in os.listdir(path):
            if os.path.isfile(os.path.join(path, file)):
                yield file


    def calc_global_stats(self):
        stats = []
        for Spieler in self.session_stats.keys():
            session_stats_P = self.session_stats[Spieler]
            
            global_stats = {}

            ## Sessions
            global_stats["Sessions_gespielt"] = len(session_stats_P)

            ## Runden
            global_stats["Runden_gespielt"] = session_stats_P["Runden"].sum()

            ## Soli
            global_stats["Soli_gespielt"] = session_stats_P["Soli"].sum()
            global_stats["Soli_gewonnen"] = session_stats_P["Soli_gewonnen"].sum()

            ## Punkte
            global_stats["Punkte_Total"] = session_stats_P["Punkte"].sum()

            ## Session Siege
            global_stats["Sessions_gewonnen"] = session_stats_P['Position'].apply(lambda x: 0 if x != 1 else 1).sum()

            ## Bestes Spiel
            global_stats["bestes_Spiel"] = session_stats_P["bestes_Spiel"].max()

            ##Bestes Spiel
            global_stats["schlechtestes_Spiel"] = session_stats_P["schlechtestes_Spiel"].min()

            stats.append(global_stats)

        return pd.DataFrame.from_records(stats, index = self.session_stats.keys())
    
    def save_globalstats_csv(self, filepath):
        self.global_stats.to_csv(Path.joinpath(filepath,'globalstats.csv'), index = False)

    def save_sessionstats_csv(self, filepath):
        for Spieler in self.session_stats.keys():
            self.global_stats[Spieler].to_csv(Path.joinpath(filepath,'sessionstats'+ Spieler +'.csv'), index = True)


