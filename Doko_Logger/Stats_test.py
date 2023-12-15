from Doko_Logger.Pages.Statistik.global_stats import Global_stats
from Pages.Statistik.Plotter import Graph
from datetime import datetime
import pandas as pd
import os

def GlobalstatsTest():
    stats = Global_stats(f".\\Test_Sessions\\")
    print(stats.Spieler)
    print(stats.session_stats)
    print(os.getcwd())
    stats.save_sessionstats_csv(os.getcwd())

    

GlobalstatsTest()