import matplotlib

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import matplotlib.animation as animation
from matplotlib import style
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import mpl_finance
from mpl_finance import candlestick_ohlc

import pandas as pd
import numpy as np

plt.style.use("default")

dateParse = lambda x: pd.datetime.strptime(x, "%Y-%m-%d %H-%p")
df = pd.read_csv("Gdax_BTCUSD_1h.csv", parse_dates=["Date"], date_parser=dateParse, index_col=0)
#print(df.head())

# RESAMPLING
df_ohlc = df["Close"].resample("1D").ohlc()
df_volume = df["Volume To"].resample("1D").sum()
#print(df_ohlc.head())

# WE NEED THE DATES CONVERTED TO MDATES IN A NEW COLUMN
df_ohlc.reset_index(inplace=True) # remove current index
df_ohlc["Date"] = df_ohlc["Date"].map(mdates.date2num)

ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=ax1)
ax1.xaxis_date() # shpw mdates as readable normal date

candlestick_ohlc(ax1, df_ohlc.values, width=2, colorup="g", colordown="r")
ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0) # X, Y, 0is where Y will flow from

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

this = new_date
print(this)

'''