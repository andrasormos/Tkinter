import pandas as pd
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
import numpy as np
import urllib
import json
import datetime as dt

from GameEngine import PlayGame

#   {} - alt + 7
#   [] - alt + 8
#   & - alt + 1
#   # - alt +shift + 3
#   \ - alt + ü
#   > < - alt + shift + Y    or X but that kills window<
#   * - alt + shift + ?

GE = PlayGame()
GE.startGame()
df_segment = GE.getChartData()
fullBalance = GE.fullBalance
cashBalance = GE.cashBalance
btcBalance = GE.BTC_Balance
currentDate = GE.endDate
currentBTCPrice = GE.currentBTCPrice
initialBalance = GE.initialBalance

rekt = True

nextRow = pd.DataFrame

showDates = True

# STYLING
LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 8)
style.use("ggplot")
fig = plt.figure(1)

# CANDLE
candleType = "1D"
candleWidth = 0.5
darkColor = "#824B4B"
lightColor = "#4B8251"
volumeColor = "#7CA1B4"

# THESE ARE DEFAULTS WHICH THE USER CAN CHANGE LATER
exchange = "GDAX_BTCUSD"
resampleSize = "15Min"

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
    candleType = type
    candleWidth = width
    print("Changed To:",type)
    changeCandle()

def action(action):
    global nextRow
    global rekt
    global done

    if action == "Skip 4x":
        for _ in range(0, 3):
            nextRow, rekt, done, reward = GE.nextStep(action)
            getNewData()

    elif action == "Skip 48x":
        for _ in range(0, 47):
            nextRow, rekt, done, reward = GE.nextStep(action)
            getNewData()

    elif action == "Skip 168x":
        for _ in range(0, 167):
            nextRow, rekt, done, reward = GE.nextStep(action)
            getNewData()
    else:
        nextRow, rekt, done, reward = GE.nextStep(action)
        getNewData()

    if rekt == True:
        popupmsg("YOU'RE REKT!")

    if done == True:
        msg = ("YOU WON THE GAME AND MADE $", str(fullBalance - initialBalance))
        popupmsg(msg)

    updateChart()

def getNewData():
    global df_segment
    global rekt

    df_segment = pd.concat([nextRow, df_segment])


def changeCandle():
    plt.clf()

    if candleType == "1H":
        ax1 = plt.subplot2grid((6, 1), (0, 0), rowspan=5, colspan=1)
        ax2 = plt.subplot2grid((6, 1), (5, 0), rowspan=1, colspan=1, sharex=ax1)
        plt.setp(ax1.get_xticklabels(), visible=False)

        df_ohlc = df_segment["Close"]
        df_volume = df_segment["Volume To"].resample(candleType).sum()
        df_ohlc.reset_index(inplace=True)
        df_ohlc["Date"] = df_ohlc["Date"].map(mdates.date2num)

        ax1.xaxis_date()  # show mdates as readable normal date
        plt.plt(ax1)
        ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0, facecolors=volumeColor)
        fig.canvas.draw()

    else:
        ax1 = plt.subplot2grid((6, 1), (0, 0), rowspan=5, colspan=1)
        ax2 = plt.subplot2grid((6, 1), (5, 0), rowspan=1, colspan=1, sharex=ax1)
        plt.setp(ax1.get_xticklabels(), visible=False)

        df_ohlc = df_segment["Close"].resample(candleType).ohlc()
        df_volume = df_segment["Volume To"].resample(candleType).sum()
        df_ohlc.reset_index(inplace=True)
        df_ohlc["Date"] = df_ohlc["Date"].map(mdates.date2num)

        ax1.xaxis_date()  # show mdates as readable normal date
        candlestick_ohlc(ax1, df_ohlc.values, width=candleWidth, colorup=lightColor, colordown=darkColor)
        ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0, facecolors=volumeColor)
        fig.canvas.draw()


def updateChart():
    global endDate
    global df_segment
    global fullBalance
    global cashBalance
    global btcBalance
    global currentDate
    global currentBTCPrice
    global fullBalance

    plt.clf()
    ax1 = plt.subplot2grid((6, 1), (0, 0), rowspan=5, colspan=1)
    ax2 = plt.subplot2grid((6, 1), (5, 0), rowspan=1, colspan=1, sharex=ax1)
    plt.setp(ax1.get_xticklabels(), visible=False)

    #df_segment = pd.concat([nextRow, df_segment])
    df_ohlc = df_segment["Close"].resample(candleType).ohlc()
    df_volume = df_segment["Volume To"].resample(candleType).sum()
    df_ohlc.reset_index(inplace=True)
    df_ohlc["Date"] = df_ohlc["Date"].map(mdates.date2num)

    ax1.xaxis_date()  # show mdates as readable normal date
    candlestick_ohlc(ax1, df_ohlc.values, width=candleWidth, colorup=lightColor, colordown=darkColor)
    ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0, facecolors=volumeColor)
    fig.canvas.draw()

    fullBalance = GE.fullBalance
    cashBalance = GE.cashBalance
    btcBalance = GE.BTC_Balance
    currentDate = GE.endDate
    currentBTCPrice = GE.currentBTCPrice
    fullBalance = GE.fullBalance

    app.gamePage.updateBalance(fullBalance, cashBalance, btcBalance, currentDate, currentBTCPrice)

def drawChart():
    try:
        if exchange == "GDAX_BTCUSD":
            plt.clf()
            ax1 = plt.subplot2grid((6, 1), (0, 0), rowspan=5, colspan=1)
            ax2 = plt.subplot2grid((6, 1), (5, 0), rowspan=1, colspan=1, sharex=ax1)
            plt.setp(ax1.get_xticklabels(), visible=False)

            if showDates == False:
                plt.setp(ax2.get_xticklabels(), visible=False)

            df_ohlc = df_segment["Close"].resample(candleType).ohlc()
            df_volume = df_segment["Volume To"].resample(candleType).sum()
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

        tk.Tk.config(self, menu=menubar)
        self.frames = {}

        self.gamePage = BTCe_Page(container, self)
        self.gamePage.grid(row=0, column=0, sticky="nsew")
        self.gamePage.tkraise()

    def show_frame(self, cont):  # bings chosen frame to the front
        frame = self.frames[BTCe_Page]
        frame.tkraise()  # bring frame to the front

class BTCe_Page(tk.Frame):

    def updateBalance(self, fullBalance, cashBalance, btc, currentDate ,currentBTCPrice):
        self.TOTAL_Balance_val_lbl.configure(text=("$", str(fullBalance) ))
        self.USD_Balance_val_lbl.configure(text=("$", str(cashBalance) ))
        self.BTC_Balance_val_lbl.configure(text=btc)
        if showDates == True:
            self.currentDate_val_lbl.configure(text=(str(currentDate))[:16])
        else:
            self.currentDate_val_lbl.configure(text=(str(currentDate))[8:16])
        self.currentBTCPrice_val_lbl.configure(text=("$", str(currentBTCPrice) ))
        self.profit_val_lbl.configure(text=("$", str(fullBalance - 5000) ))

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
        #candle1H = ttk.Button(ctr_left, text="1 Hour", command=lambda: changeCandleType("1H", 0.032))
        candle4H = ttk.Button(ctr_left, text="4 Hours", command=lambda: changeCandleType("4H", 0.08))
        candle1D = ttk.Button(ctr_left, text="1 Day", command=lambda: changeCandleType("1D", 0.5))
        candle1W = ttk.Button(ctr_left, text="1 Week", command=lambda: changeCandleType("1W", 5))

        candle_time.grid(row=0, columnspan=3,padx=10, pady=10)
        #candle1H.grid(row=1, columnspan=3)
        candle4H.grid(row=2, columnspan=3)
        candle1D.grid(row=3, columnspan=3)
        candle1W.grid(row=4, columnspan=3)

        updateButton = ttk.Button(ctr_left, text="Update", command=lambda:popupmsg("REKT")).grid(row=11, columnspan=3)

        # RIGHT DATE COLUMN
        currentDate_lbl = ttk.Label(ctr_right, text='DATE:')
        if showDates == True:
            self.currentDate_val_lbl = ttk.Label(ctr_right, text=currentDate[:16])
        else:
            self.currentDate_val_lbl = ttk.Label(ctr_right, text=currentDate[8:16])
        currentBTCPrice_lbl = ttk.Label(ctr_right, text='BTC PRICE:')
        self.currentBTCPrice_val_lbl = ttk.Label(ctr_right, text=("$", str(currentBTCPrice) ))

        # PLACEMENT
        currentDate_lbl.grid(row=19, column=0, columnspan=1, pady=5, sticky="w")
        self.currentDate_val_lbl.grid(row=19, column=1, columnspan=1, sticky="e")
        currentBTCPrice_lbl.grid(row=20, column=0, columnspan=1, pady=5, sticky="w")
        self.currentBTCPrice_val_lbl.grid(row=20, column=1, columnspan=1, sticky="e")


        # RIGHT BUTTON COLUMN
        TOTAL_Balance_lbl = ttk.Label(ctr_right, text='TOTAL WORTH:')
        self.TOTAL_Balance_val_lbl = ttk.Label(ctr_right, text=("$", str(fullBalance) ))
        profit_lbl = ttk.Label(ctr_right, text='Profit:')
        self.profit_val_lbl = ttk.Label(ctr_right, text=(fullBalance - 5000))
        USD_Balance_lbl = ttk.Label(ctr_right, text='CASH WALLET:')
        self.USD_Balance_val_lbl = ttk.Label(ctr_right, text=("$", str(cashBalance) ))
        BTC_Balance_lbl = ttk.Label(ctr_right, text='BTC WALLET:')
        self.BTC_Balance_val_lbl = ttk.Label(ctr_right, text=btcBalance)

        tradeBTC_lbl = ttk.Label(ctr_right, text='TRADE')
        buyBTC_btn = ttk.Button(ctr_right, text="BUY BTC for $500", command=lambda: action("Buy BTC"))
        sellBTC_btn = ttk.Button(ctr_right, text="SELL BTC for $500", command=lambda: action("Sell BTC"))

        skip_lbl = ttk.Label(ctr_right, text='Skip Forward')
        skip_btn = ttk.Button(ctr_right, text="Skip Hour", command=lambda: action("Skip 1x"))
        skip4x_btn = ttk.Button(ctr_right, text="Skip 4 Hours", command=lambda: action("Skip 4x"))
        skip48x_btn = ttk.Button(ctr_right, text="Skip 2 Days", command=lambda: action("Skip 48x"))
        skip168x_btn = ttk.Button(ctr_right, text="Skip 1 Week", command=lambda: action("Skip 168x"))

        # PLACEMENT
        TOTAL_Balance_lbl.grid(row=21, column=0, columnspan=1, pady=30, sticky="w")
        self.TOTAL_Balance_val_lbl.grid(row=21, column=1, columnspan=1, sticky="e")
        profit_lbl.grid(row=22, column=0, columnspan=1, pady=30, sticky="w")
        self.profit_val_lbl.grid(row=22, column=1, columnspan=1, sticky="e")

        USD_Balance_lbl.grid(row=23, column=0, columnspan=1, pady=5, sticky="w")
        self.USD_Balance_val_lbl.grid(row=23, column=1, columnspan=1, sticky="e")

        BTC_Balance_lbl.grid(row=24, column=0, columnspan=1, pady=5, sticky="w")
        self.BTC_Balance_val_lbl.grid(row=24, column=1, columnspan=1, sticky="e")

        tradeBTC_lbl.grid(row=25, columnspan=1, pady=10)
        buyBTC_btn.grid(row=26, columnspan=1)
        sellBTC_btn.grid(row=27, columnspan=1)

        skip_lbl.grid(row=28, columnspan=1, pady=10)
        skip_btn.grid(row=29, columnspan=1)
        skip4x_btn.grid(row=30, columnspan=1)
        skip48x_btn.grid(row=31, columnspan=1)
        skip168x_btn.grid(row=32, columnspan=1)



app = SeaofBTCapp()
app.geometry("1280x720")
test = drawChart()

app.mainloop()




