import tkinter as tk
from tkinter import ttk
import matplotlib
import datetime as dt

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

# failed in the non-tick animate:  'Timestamp' object has no attribute 'to_pydatetme'

#   {} - alt + 7
#   [] - alt + 8
#   & - alt + 1
#   # - alt +shift + 3
#   \ - alt + ü
#   > < - alt + shift + Y    or X but that kills window<

LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 8)
style.use("ggplot")
f = plt.figure()

# MY VARIABLES
startDate = "2018-1-1 01:00:00"
endDate = "2018-2-1 01:00:00"
candleWidth = 0.5
darkColor = "#824B4B"
lightColor = "#4B8251"
volumeColor = "#7CA1B4"

# THESE ARE DEFAULTS WHICH THE USER CAN CHANGE LATER
exchange = "GDAX_BTCUSD"
DatCounter = 9000  # force an update instead of waiting 30 seconds, counter for that is this
programName = "btce"
resampleSize = "15Min"  # each candle stcik will show 15 minutes change
DataPace = "tick"

paneCount = 1
topIndicator = "none"
bottomIndicator = "none"
middleIndicator = "none"
chartLoad = True


def changeExchange(toWhat, pn):  # program name
    global exchange
    global DatCounter
    global programName  # by globalling them we can modify them

    exchange = toWhat
    programName = pn
    DatCounter = 9000


def popupmsg(msg):  # a miniature version of a tk window
    popup = tk.Tk()

    def leavemini():
        popup.destroy()

    popup.wm_title("!")
    label = ttk.Label(popup, text=msg, font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)  # padding y
    B1 = ttk.Button(popup, text="Okay", command=leavemini)
    B1.pack()  # just naturally go under the label
    popup.mainloop()


def animate(i):
    global refreshRate
    global DatCounter

    if chartLoad:
        try:
            if exchange == "GDAX_BTCUSD":
                dateParse = lambda x: pd.datetime.strptime(x, "%Y-%m-%d %H-%p")
                df = pd.read_csv("Gdax_BTCUSD_1h.csv", parse_dates=["Date"], date_parser=dateParse, index_col=0)

                df = df.loc[startDate: endDate]

                # RESAMPLING
                df_ohlc = df["Close"].resample("1D").ohlc()
                df_volume = df["Volume To"].resample("1D").sum()
                # print(df_ohlc.head())

                df_ohlc.reset_index(inplace=True)
                df_ohlc["Date"] = df_ohlc["Date"].map(mdates.date2num)

                # ax1.clear()
                # ax2.clear()

                ax1 = plt.subplot2grid((6, 1), (0, 0), rowspan=5, colspan=1)
                plt.setp(ax1.get_xticklabels(), visible=False)
                ax2 = plt.subplot2grid((6, 1), (5, 0), rowspan=1, colspan=1, sharex=ax1)
                ax1.xaxis_date()  # show mdates as readable normal date

                candlestick_ohlc(ax1, df_ohlc.values, width=candleWidth, colorup=lightColor, colordown=darkColor)
                ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0, facecolors=volumeColor)

        except Exception as e:
            print("Failed because of:", e)

        else:
            DatCounter += 1  # INCREMENT COUNTER


class SeaofBTCapp(tk.Tk):  # inherit from the tk class
    def __init__(self, *args,
                 **kwargs):  # ars - any number of variables being passed into here, kwargs - passing dictionaries
        tk.Tk.__init__(self, *args, **kwargs)

        # tk.TK.iconbitmap(self, default="icon_Name.ico")
        tk.Tk.wm_title(self, "BAWSAQ")

        container = tk.Frame(self)  # the actual main windo
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        menubar = tk.Menu(container)  # menubar is sent to container
        filemenu = tk.Menu(menubar, tearoff=0)  # filemenu is sent to menubar
        filemenu.add_command(label="Save Settings", command=lambda: popupmsg("Not supported just yet"))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=quit)
        menubar.add_cascade(label="File", menu=filemenu)  # actually assign the file to menubar

        exchangeChoice = tk.Menu(menubar, tearoff=1)
        exchangeChoice.add_command(label="GDAX_BTCUSD", command=lambda: changeExchange("GDAX_BTCUSD", "btce"))
        exchangeChoice.add_command(label="Bitfinex", command=lambda: changeExchange("Bitfinex", "bitfinex"))
        exchangeChoice.add_command(label="Bitstamp", command=lambda: changeExchange("Bitstamp", "bitstamp"))
        exchangeChoice.add_command(label="Huobi", command=lambda: changeExchange("Huobi", "huobi"))
        menubar.add_cascade(label="Exchange", menu=exchangeChoice)

        dataTF = tk.Menu(menubar, tearoff=1)  # timeframes for bars
        dataTF.add_command(label="Tick", command=lambda: changeTimeFrame("tick"))
        dataTF.add_command(label="1 Day", command=lambda: changeTimeFrame("1d"))
        dataTF.add_command(label="3 Day", command=lambda: changeTimeFrame("3d"))
        dataTF.add_command(label="1 Week", command=lambda: changeTimeFrame("7d"))
        menubar.add_cascade(label="Data Time Frame", menu=dataTF)

        OHLCI = tk.Menu(menubar, tearoff=1)
        OHLCI.add_command(label="Tick", command=lambda: changeTimeFrame("tick"))
        OHLCI.add_command(label="1 minute",
                          command=lambda: changeSampleSize("1Min", 0.0005))  # width of the candle stick
        OHLCI.add_command(label="5 minute", command=lambda: changeSampleSize("5Min", 0.003))
        OHLCI.add_command(label="15 minute", command=lambda: changeSampleSize("15Min", 0.008))
        OHLCI.add_command(label="30 minute", command=lambda: changeSampleSize("30Min", 0.016))
        OHLCI.add_command(label="1 Hour", command=lambda: changeSampleSize("1H", 0.032))
        OHLCI.add_command(label="3 Hour", command=lambda: changeSampleSize("3H", 0.096))
        menubar.add_cascade(label="OHLC Interval", menu=OHLCI)

        tk.Tk.config(self, menu=menubar)
        self.frames = {}

        for F in (StartPage, BTCe_Page):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0,
                       sticky="nsew")  # sticky is alignment north south east west, stretch everything to the sides of the window

        self.show_frame(BTCe_Page)

    def show_frame(self, cont):  # bings chosen frame to the front
        frame = self.frames[cont]
        frame.tkraise()  # bring frame to the front


class StartPage(tk.Frame):  # inherit tk.Frame so we dont have to call upon that
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label_1 = ttk.Label(self, text=("BUY BTC"), font=LARGE_FONT)
        label_2 = ttk.Label(self, text=("SELL BTC"), font=LARGE_FONT)
        button_1 = ttk.Button(self, text="BUY", command=lambda: controller.show_frame(BTCe_Page))
        button_2 = ttk.Button(self, text="SELL", command=quit)
        button_3 = ttk.Button(self, text="NaN", command=quit)

        label_1.grid(row=0, column=0, sticky="E")
        label_2.grid(row=1, column=0, sticky="E")

        button_1.grid(row=0, column=1)
        button_2.grid(row=1, column=1)
        button_3.grid(row=1, column=2)


class BTCe_Page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # create all of the main containers
        top_frame = tk.Frame(self, bg='cyan', width=450, height=50, pady=3)
        center = tk.Frame(self, bg='pink', width=50, height=40, padx=3, pady=3)
        btm_frame = tk.Frame(self, bg='white', width=450, height=45, pady=3)
        btm_frame2 = tk.Frame(self, bg='green', width=450, height=60, pady=3)

        # layout all of the main containers
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        top_frame.grid(row=0, sticky="ew")
        center.grid(row=1, sticky="nsew")
        btm_frame.grid(row=3, sticky="ew")
        btm_frame2.grid(row=4, sticky="ew")

        # create the widgets for the top frame
        label = ttk.Label(top_frame, text="Graph Page", font=LARGE_FONT)
        width_label = ttk.Label(top_frame, text='Width:')
        length_label = ttk.Label(top_frame, text='Length:')
        entry_W = ttk.Entry(top_frame, background="pink")
        entry_L = ttk.Entry(top_frame, background="orange")

        # layout the widgets in the top frame
        label.grid(row=0 ,columnspan=6, sticky="ew")
        width_label.grid(row=1, column=0)
        length_label.grid(row=1, column=2)
        entry_W.grid(row=1, column=1)
        entry_L.grid(row=1, column=3)

        # create the center widgets
        center.grid_rowconfigure(0, weight=1)
        center.grid_columnconfigure(1, weight=1)

        ctr_left = tk.Frame(center, bg='blue', width=100, height=190)
        ctr_mid = tk.Frame(center, bg='yellow', width=250, height=190, padx=3, pady=3)
        ctr_right = tk.Frame(center, bg='green', width=100, height=190, padx=3, pady=3)

        ctr_left.grid(row=0, column=0, sticky="ns")
        ctr_mid.grid(row=0, column=1, sticky="nsew")
        ctr_right.grid(row=0, column=2, sticky="ns")



        button1 = ttk.Button(ctr_mid, text="Back to Home", command=lambda: controller.show_frame(StartPage))
        button1.grid(row=0, columnspan=3)

        '''
        label = ttk.Label(self, text="Graph Page", font=LARGE_FONT)  # this is just an object that we defined, we havent done anything with it yet
        label.pack(pady=10, padx=10)
        button1 = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage))
        button1.pack()

        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2TkAgg(canvas, self)  # we are sending the toolbar to the canvas
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        '''


app = SeaofBTCapp()
app.geometry("1280x720")
ani = animation.FuncAnimation(f, animate, interval=2000)
app.mainloop()



