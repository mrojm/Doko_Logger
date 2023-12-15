import os
import pandas as pd
from datetime import datetime

from SessionHandler.session import Session
from Statistik.figure import make_fig
from Statistik.plotwindow import PlotWindow


class Statistiken:
    
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

        self.__load_sessions(session_folder_path, start_date, end_date)
        self.Spieler = list(self.session_stats.index.droplevel(level=1).drop_duplicates())

        self.global_stats = self.get_all_global_stats()
    

    ##
    ## Global Stuff erstellen
    ##
    def get_all_global_stats(self):
        data = [self.get_global_Runden_column(self.Spieler).stack().rename("Runden"),
                self.get_global_Punkte_column(self.Spieler).stack().rename("Punkte"),
                self.get_global_Soli_column(self.Spieler).stack().rename("Soli"), 
                self.get_global_Soligewonnen_column(self.Spieler).stack().rename("Soli_g"),
                self.get_global_Siege_column(self.Spieler).stack().rename("Siege"),
                self.get_global_BestesSpiel_column(self.Spieler).stack().rename("BSpiel"),
                self.get_global_SchlechtestesSpiel_column(self.Spieler).stack().rename("SSpiel")]
        
        return pd.DataFrame(data).transpose().swaplevel().sort_index()

    def get_global_Runden_column(self, Spieler):
        return self.session_stats.loc[Spieler]["Runden"].unstack(level=0).cumsum()
    
    def get_global_Punkte_column(self,Spieler):
        return self.session_stats.loc[Spieler]["Punkte"].unstack(level=0).cumsum()
            
    def get_global_Soli_column(self,Spieler):
        return self.session_stats.loc[Spieler]["Soli"].unstack(level=0).cumsum()
    
    def get_global_Soligewonnen_column(self,Spieler):
        return self.session_stats.loc[Spieler]["Soli_gewonnen"].unstack(level=0).cumsum()
    
    def get_global_Siege_column(self,Spieler):
        Series = self.session_stats.loc[Spieler]["Position"].apply(lambda x: 0 if x != 1 else 1)
        return Series.unstack(level=0).cumsum()
       
    def get_global_BestesSpiel_column(self,Spieler):
        return self.session_stats.loc[Spieler]["bestes_Spiel"].unstack(level=0).cummax()
      
    def get_global_SchlechtestesSpiel_column(self,Spieler):
        return self.session_stats.loc[Spieler]["schlechtestes_Spiel"].unstack(level=0).cummin()

    
    ##
    ## Sessions laden
    ##

    def __load_sessions(self, session_folder_path, start_date, end_date):
        # Für jede Session im Ordner

        session_stats_list = []
        for sessionname in self.__get_sessions(session_folder_path):
            
            #Session erstellen und laden
            session = Session(sessionname, session_folder_path, add_json=False)
            session.load_session()
            
            #Check if Session empty
            if len(session.Punkte.df) == 0:
                continue

            self.sessions.append(session)

            session_stats = session.Results()
            # Spieler laden und Dataframe erstellen
            for Spieler in session_stats:
                # Sessionstats ablegen
                session_stats[Spieler]["Name"] = Spieler
                session_stats_list.append(session_stats[Spieler])

            df = pd.DataFrame.from_records(session_stats_list).set_index(["Name","Datum"]).sort_index()

            self.session_stats = df.loc[pd.IndexSlice[:,start_date: end_date],:]
                 
    @staticmethod
    def __get_sessions(path):
        for file in os.listdir(path):
            if os.path.isfile(os.path.join(path, file)):
                yield file
   
    
    ##
    ## TABELLEN SPEICHERN
    ##
    def save_globalstats_csv(self, filepath):
        self.global_stats.to_csv(filepath +'\\sessionstats.csv', index = True, sep=";")

    def save_sessionstats_csv(self, filepath):
        self.session_stats.to_csv(filepath +'\\sessionstats.csv', index = True, sep=";")

    
    ##
    ## PLOT FUNCTIONS
    ##        
    
    def RundenPlot(self):
        PlotWindow(make_fig(self.get_global_Runden_column(self.Spieler), "Runden gespielt"))

    def PunktePlot(self):
        PlotWindow(make_fig(self.get_global_Punkte_column(self.Spieler), "Punkte Total"))
        
    def SiegePlot(self):
        PlotWindow(make_fig(self.get_global_Siege_column(self.Spieler), "Session Siege"))

    def SoliPlot(self):
        PlotWindow(make_fig(self.get_global_Soli_column(self.Spieler), "Soli gespielt"))

    def SoliGewonnenPlot(self):
        PlotWindow(make_fig(self.get_global_Soligewonnen_column(self.Spieler), "Soli gewonnen"))

    def BestesSpielPlot(self):
        PlotWindow(make_fig(self.get_global_BestesSpiel_column(self.Spieler), "Bestes Spiel"))

    def SchlechtestesSpielPlot(self):
        PlotWindow(make_fig(self.get_global_SchlechtestesSpiel_column(self.Spieler), "Schlechtestes Spiel"))
        
