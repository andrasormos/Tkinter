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

from GameEngine import PlayGame
#import GameEngine as GE

gameEngine = PlayGame()
gameEngine.startGame()


#test.printFromClass()

#   {} - alt + 7
#   [] - alt + 8
#   & - alt + 1
#   # - alt +shift + 3
#   \ - alt + ü
#   > < - alt + shift + Y    or X but that kills window<

# STYLING
LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 8)
style.use("ggplot")
fig = plt.figure(1)

# MY VARIABLES

candleType = "4H"
candleWidth = 0.08
darkColor = "#824B4B"
lightColor = "#4B8251"
volumeColor = "#7CA1B4"

startDate = gameEngine.getStartDate()
endDate = gameEngine.getEndDate()

dateParse = lambda x: pd.datetime.strptime(x, "%Y-%m-%d %I-%p")
df_orig = pd.read_csv("Gdax_BTCUSD_1h.csv", parse_dates=["Date"], date_parser=dateParse, index_col=0)
df = df_orig.loc[startDate : endDate]


# THESE ARE DEFAULTS WHICH THE USER CAN CHANGE LATER
exchange = "GDAX_BTCUSD"
DatCounter = 9000  # force an update instead of waiting 30 seconds, counter for that is this
resampleSize = "15Min"  # each candle stcik will show 15 minutes change
DataPace = "tick"

paneCount = 1
topIndicator = "none"
bottomIndicator = "none"
middleIndicator = "none"
chartLoad = True

def action(action):
    updateChart()

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

def changeCandleType(type, width):
    global candleType
    global candleWidth
    global DatCounter
    candleType = type
    candleWidth = width
    DatCounter = 9000
    print("Changed To:",type)
    updateChart()

def updateChart():
    global endDate
    plt.clf()
    ax1 = plt.subplot2grid((6, 1), (0, 0), rowspan=5, colspan=1)
    ax2 = plt.subplot2grid((6, 1), (5, 0), rowspan=1, colspan=1, sharex=ax1)
    plt.setp(ax1.get_xticklabels(), visible=False)

    endDate = gameEngine.nextStep(action)
    print("NEXT TIME HOUR:", df_orig[endDate])
    #print(df)


    #nextLine = df_orig[endDate]
    #nextLine = nextLine.join(df)
    # how to append or join dataframes together

    # This one works but might be a slow solution
    df = df_orig.loc[startDate: endDate]

    # RESAMPLING
    df_ohlc = df["Close"].resample(candleType).ohlc()
    df_volume = df["Volume To"].resample(candleType).sum()
    # print(df_ohlc.head())

    df_ohlc.reset_index(inplace=True)
    df_ohlc["Date"] = df_ohlc["Date"].map(mdates.date2num)

    ax1.xaxis_date()  # show mdates as readable normal date
    candlestick_ohlc(ax1, df_ohlc.values, width=candleWidth, colorup=lightColor, colordown=darkColor)
    ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0, facecolors=volumeColor)

    fig.canvas.draw()


def drawChart():
    try:
        if exchange == "GDAX_BTCUSD":
            plt.clf()
            ax1 = plt.subplot2grid((6, 1), (0, 0), rowspan=5, colspan=1)
            ax2 = plt.subplot2grid((6, 1), (5, 0), rowspan=1, colspan=1, sharex=ax1)
            plt.setp(ax1.get_xticklabels(), visible=False)

            # RESAMPLING
            df_ohlc = df["Close"].resample(candleType).ohlc()
            df_volume = df["Volume To"].resample(candleType).sum()
            # print(df_ohlc.head())

            df_ohlc.reset_index(inplace=True)
            df_ohlc["Date"] = df_ohlc["Date"].map(mdates.date2num)

            ax1.xaxis_date()  # show mdates as readable normal date
            candlestick_ohlc(ax1, df_ohlc.values, width=candleWidth, colorup=lightColor, colordown=darkColor)
            ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0, facecolors=volumeColor)

            fig.canvas.draw()

    except Exception as e:
        print("Failed because of:", e)

class SeaofBTCapp(tk.Tk):  # inherit from the tk class
    def __init__(self, *args, **kwargs):  # ars - any number of variables being passed into here, kwargs - passing dictionaries
        tk.Tk.__init__(self, *args, **kwargs)

        # tk.TK.iconbitmap(self, default="icon_Name.ico")
        tk.Tk.wm_title(self, "BAWSAQ")

        container = tk.Frame(self)  # the actual main windo
        container.pack(side="top", fill="both", expand=True)
        #container.grid(row=1, sticky="nsew")

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

    def recreatePage(self):
        BTCe_Page.destroy()
        print("WORKS Yeha!")

class StartPage(tk.Frame):  # inherit tk.Frame so we dont have to call upon that
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label_1 = ttk.Label(self, text=("TRADE FROM HISTORICAL CHART DATA"), font=LARGE_FONT)
        button_1 = ttk.Button(self, text="NEW GAME", command=lambda: controller.show_frame(BTCe_Page))
        button_2 = ttk.Button(self, text="QUIT", command=quit)

        label_1.grid(row=0, column=0, sticky="E")
        button_1.grid(row=0, column=1)
        button_2.grid(row=1, column=1)

class BTCe_Page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # MAIN CONTAINER CREATION
        top_frame = tk.Frame(self, bg='white', width=450, height=50, pady=3)
        center = tk.Frame(self, bg='gray2', width=50, height=40, padx=3, pady=3)
        btm_frame = tk.Frame(self, bg='white', width=450, height=45, pady=3)
        btm_frame2 = tk.Frame(self, bg='lavender', width=450, height=60, pady=3)
        # ROWCONFIGURE
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        # PLACE MAIN CONTAINERS
        top_frame.grid(row=0, sticky="nsew")
        top_frame.grid_rowconfigure(0, weight=1)
        top_frame.grid_columnconfigure(1, weight=1)

        center.grid(row=1, sticky="nsew")
        btm_frame.grid(row=3, sticky="ew")
        btm_frame2.grid(row=4, sticky="ew")

        # TOP FRAME
        Title = ttk.Label(top_frame, text='BTC Price')
        Title.grid_rowconfigure(1, weight=1)
        Title.grid_columnconfigure(0, weight=1)

        # PLACE WIDGETS TO TOP FRAME
        Title.grid(row=0, columnspan=3, sticky="nsew")

        # ROWCONFIGURE - CENTER
        center.grid_rowconfigure(0, weight=1)
        center.grid_columnconfigure(1, weight=1)
        # CENTER FRAME
        ctr_left = tk.Frame(center, bg='white', width=100, height=190)
        ctr_mid =  tk.Frame(center, bg='white', width=250, height=190, padx=3, pady=3)
        ctr_right = tk.Frame(center, bg='white', width=100, height=190, padx=3, pady=3)

        # PLACE CENTER FRAMES
        ctr_left.grid(row=0, column=0, sticky="ns")

        ctr_mid.grid(row=0, column=1, sticky="nsew")
        ctr_mid.grid_rowconfigure(0, weight=1)
        ctr_mid.grid_columnconfigure(1, weight=1)

        ctr_right.grid(row=0, column=2, sticky="ns")

        # MID COLUMN - GRAPH
        graph = FigureCanvasTkAgg(fig, ctr_mid)
        graph.get_tk_widget().grid(row=0, column=1, sticky="nsew")

        # LEFT BUTTON COLUMN
        candle_time = ttk.Label(ctr_left, text='Candle Time')
        candle1H = ttk.Button(ctr_left, text="1 Hour", command=lambda: changeCandleType("1H", 0.032))
        candle4H = ttk.Button(ctr_left, text="4 Hours", command=lambda: changeCandleType("4H", 0.08))
        candle1D = ttk.Button(ctr_left, text="1 Day", command=lambda: changeCandleType("1D", 0.5))
        candle1W = ttk.Button(ctr_left, text="1 Week", command=lambda: changeCandleType("1W", 5))

        candle_time.grid(row=0, columnspan=3,padx=10, pady=10)
        candle1H.grid(row=1, columnspan=3)
        candle4H.grid(row=2, columnspan=3)
        candle1D.grid(row=3, columnspan=3)
        candle1W.grid(row=4, columnspan=3)

        updateButton = ttk.Button(ctr_left, text="Update", command=lambda:updateChart()).grid(row=11, columnspan=3)

        # RIGHT BUTTON COLUMN
        tradeBTC_lbl = ttk.Label(ctr_right, text='TRADE')
        buyBTC_btn = ttk.Button(ctr_right, text="BUY BTC", command=lambda: action("Buy BTC"))
        sellBTC_btn = ttk.Button(ctr_right, text="SELL BTC", command=lambda: action("Sell BTC"))
        skip_btn = ttk.Button(ctr_right, text="SKIP", command=lambda: action("Skip"))

        tradeBTC_lbl.grid(row=0, columnspan=3,padx=10, pady=10)
        buyBTC_btn.grid(row=1, columnspan=3)
        sellBTC_btn.grid(row=2, columnspan=3)
        skip_btn.grid(row=3, columnspan=3)

        tradeBTC_lbl.grid(row=6, columnspan=3, padx=10, pady=10)
        buyBTC_btn.grid(row=7, columnspan=3)
        sellBTC_btn.grid(row=8, columnspan=3)
        skip_btn.grid(row=9, columnspan=3)


app = SeaofBTCapp()
app.geometry("1280x720")
test = drawChart()

app.mainloop()



