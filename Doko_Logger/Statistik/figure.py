from matplotlib import ticker, dates
from matplotlib.figure import Figure

def make_fig(data, title):
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.set_title(title)

        ax.plot(data, label = data.columns, marker = 'o')

        ax.yaxis.set_major_locator(ticker.AutoLocator())
        ax.xaxis.set_major_locator(dates.AutoDateLocator(maxticks=5, minticks=2, interval_multiples=True))
        ax.xaxis.set_major_formatter(dates.DateFormatter(fmt = '%d-%m-%Y'))
        ax.grid()
        
        ax.legend(loc = "best")
        return fig