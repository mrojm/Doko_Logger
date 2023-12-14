from Pages.Datahandling.global_stats import Global_stats
from Pages.Plots.stats_figures import Stat_Fig
from Pages.Plots.Plotter import Graph
from datetime import datetime
import pandas as pd

def GlobalstatsTest():
    stats = Global_stats(f".\\Test_Sessions\\")

    print(stats.session_stats)
    print(stats.get_global_Soli_column("A"))

    #print(stats.session_stats["A"])
    #print(stats.global_stats)

def stats_figuresTest():
    figures = Stat_Fig(end_date=datetime(2023,12,16))
    Graph(figures.test())
    

GlobalstatsTest()
#stats_figuresTest()

#df = pd.DataFrame.from_records([{"First": "A","SECOND":1, "DATA1":1},{"First": "A","SECOND":2, "DATA1":2},{"First": "B","SECOND":1, "DATA1":1},{"First": "B","SECOND":2, "DATA1":2}]).set_index(["First","SECOND"])