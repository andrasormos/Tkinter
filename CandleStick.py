import tkinter as tk
from tkinter import ttk
import matplotlib

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import mpl_finance
from mpl_finance import candlestick_ohlc
import urllib
import json
import pandas as pd
import numpy as np

plt.style.use("default")

dateParse = lambda x: pd.datetime.strptime(x, "%Y-%m-%d %H-%p")
df = pd.read_csv("Gdax_BTCUSD_1h.csv", parse_dates=["Date"], date_parser=dateParse, index_col=0)


print(df.head())


df["Close"].plot()

#df.plot()
plt.show()



'''

# Read Into Pandas
date_data = df["Date"]
open_data = df["Open"]
high_data = df["High"]
low_data = df["Low"]
close_data = df["Close"]
trade = []
turn = []




date_data = np.array(date_data)
new_date = dates.datestr2num(date_data)



this = new_date
print(this)

'''