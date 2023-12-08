from points import Points
import pandas as pd
import numpy as np

Spieler = ["A", "B", "C", "D", "E"]
points = Points(Spieler)

#test1 = points.format_entry({"Spiel":1, "Spieler":["A","B","C","D"], "Gewinner":["A"], "Punkte":2, "Bockrunden":2, "Spieltyp":"Normalspiel"})
points.add_entry({"Spiel":1, "Spieler":["A","B","C","D"], "Gewinner":["A"], "Punkte":2, "Bockrunden":2, "Spieltyp":"Solo"})
points.add_entry({"Spiel":2, "Spieler":["A","D","C","E"], "Gewinner":["A"], "Punkte":2, "Bockrunden":2, "Spieltyp":"Solo"})
points.add_entry({"Spiel":3, "Spieler":["A","B","C","D"], "Gewinner":["A"], "Punkte":2, "Bockrunden":2, "Spieltyp":"Solo"})
points.add_entry({"Spiel":4, "Spieler":["A","B","C","D"], "Gewinner":["A"], "Punkte":2, "Bockrunden":2, "Spieltyp":"Solo"})
points.add_entry({"Spiel":5, "Spieler":["A","B","C","D"], "Gewinner":["A"], "Punkte":2, "Bockrunden":2, "Spieltyp":"Solo"})
points.add_entry({"Spiel":6, "Spieler":["A","B","C","D"], "Gewinner":["A"], "Punkte":2, "Bockrunden":2, "Spieltyp":"Solo"})

print(points.df)

