from Datahandling.global_stats import Global_stats

from matplotlib import ticker, dates


from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from datetime import datetime
import numpy as np

class Stat_Fig:
    def __init__(self, start_date=datetime(1990,1,1), end_date = datetime.today()):
        self.stats = Global_stats(".\\Test_Sessions\\", start_date=start_date, end_date=end_date)
        return

    def test(self):
        
        Spieler = list(self.stats.session_stats.keys())[0]
        data = self.stats.session_stats[Spieler]

        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.yaxis.set_major_locator(ticker.AutoLocator())
        ax.xaxis.set_major_locator(dates.AutoDateLocator(maxticks=4))
        ax.xaxis.set_major_formatter(dates.DateFormatter(fmt = '%d-%m-%Y'))

        x = data.index.to_list()
        y = data["Punkte"].to_list()

        print(x)
        print(y)
        ax.plot(x, y, marker='o', label = Spieler)
        ax.legend()
        return fig
    
    