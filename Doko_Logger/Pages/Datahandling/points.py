import pandas as pd
import numpy as np

class Points:

    def __init__(self, Spieler):
        self.Spieleranzahl = len(Spieler)


        #Dataframe erzeugen
        self.index = ["Spiel"]
        self.data_columns= ["Spiel", "Bockrunden", "Punkte", "Spieltyp"]
        self.Spieler = Spieler

        self.df_columns = ["Spiel", "Runde", "Bockrunden", "Punkte", *Spieler, "Spieltyp"]

        #pd.Series(np.zeros((1,len(Spieler)+3),int))

        self.df = pd.DataFrame(columns=self.df_columns)
        #self.df.set_index("Spiel")

    @staticmethod
    def calc_points(data:dict):
        points = {}
        Spieler = data["Spieler"]
        Spielmodus = "Normal"

        if len(data["Gewinner"]) ==1:
            Spielmodus = "Solo_gewonnen"
        if len(data["Gewinner"]) ==3:
            Spielmodus = "Solo_verloren"

        for P in Spieler:
            if P in data["Gewinner"]:
                points[P] = data["Punkte"] * 2**data["Bockrunden"]
                if Spielmodus == "Solo_gewonnen":
                    points[P] *= 3
            else:
                points[P] = -1* data["Punkte"] * 2**data["Bockrunden"]
                if Spielmodus == "Solo_verloren":
                    points[P] *= 3
        
        return points
    
    def format_entry(self, data:dict):
        points = self.calc_points(data)
        series = pd.Series(np.zeros(len(self.Spieler),int), index = self.Spieler).astype(int)
        series = series.add(pd.Series(points).astype(int), fill_value=0).astype(int)
        if len(self.df)>0:
            series = series.add(self.df.loc[len(self.df)-1][self.Spieler])

        for index in self.data_columns:
            series[index]=data[index]
        
        series["Runde"] = 1 + (series["Spiel"]-1) // self.Spieleranzahl

        return series
    
    def add_entry(self, data:dict):
        entry = self.format_entry(data)
        self.df.loc[len(self.df)] = entry