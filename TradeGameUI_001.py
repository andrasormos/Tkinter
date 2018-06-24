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

# STYLING
LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 8)
style.use("ggplot")
fig = plt.figure()

# MY VARIABLES
startDate = "2018-1-1 01:00:00"
endDate = "2018-2-1 01:00:00"
candleWidth = 0.5
darkColor = "#824B4B"
lightColor = "#4B8251"
volumeColor = "#7CA1B4"
timeSpan = "1M"
candleType = "1D"


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

def cunt():
    print("Cunt")

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

def changeCandleType(type):
    global candleType
    global DatCounter
    candleType = type
    DatCounter = 9000
    #plt.clf()

def animate(i):
    global refreshRate
    global DatCounter

    print("DatCounter:",DatCounter)

    if chartLoad:
        if DatCounter > 0:
            try:
                if exchange == "GDAX_BTCUSD":
                    print("New Graph")
                    #plt.clf()

                    ax1 = plt.subplot2grid((6, 1), (0, 0), rowspan=5, colspan=1)
                    ax2 = plt.subplot2grid((6, 1), (5, 0), rowspan=1, colspan=1, sharex=ax1)

                    plt.setp(ax1.get_xticklabels(), visible=False)

                    dateParse = lambda x: pd.datetime.strptime(x, "%Y-%m-%d %H-%p")
                    df = pd.read_csv("Gdax_BTCUSD_1h.csv", parse_dates=["Date"], date_parser=dateParse, index_col=0)
                    df = df.loc[startDate: endDate]

                    # RESAMPLING
                    df_ohlc = df["Close"].resample(candleType).ohlc()
                    df_volume = df["Volume To"].resample(candleType).sum()
                    # print(df_ohlc.head())

                    df_ohlc.reset_index(inplace=True)
                    df_ohlc["Date"] = df_ohlc["Date"].map(mdates.date2num)

                    ax1.clear()

                    ax1.xaxis_date()  # show mdates as readable normal date
                    candlestick_ohlc(ax1, df_ohlc.values, width=candleWidth, colorup=lightColor, colordown=darkColor)
                    ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0, facecolors=volumeColor)



                    DatCounter = 0  # RESET COUNTER

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
        top_frame = tk.Frame(self, bg='cyan', width=450, height=50, pady=3)
        center = tk.Frame(self, bg='gray2', width=50, height=40, padx=3, pady=3)
        btm_frame = tk.Frame(self, bg='white', width=450, height=45, pady=3)
        btm_frame2 = tk.Frame(self, bg='lavender', width=450, height=60, pady=3)
        # ROWCONFIGURE
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        # PLACE MAIN CONTAINERS
        top_frame.grid(row=0, sticky="ew")
        center.grid(row=1, sticky="nsew")
        btm_frame.grid(row=3, sticky="ew")
        btm_frame2.grid(row=4, sticky="ew")

        # TOP FRAME
        model_label = ttk.Label(top_frame, text='Model Dimensions')
        width_label = ttk.Label(top_frame, text='Width:')
        length_label = ttk.Label(top_frame, text='Length:')
        entry_W = ttk.Entry(top_frame, background="pink")
        entry_L = ttk.Entry(top_frame, background="orange")
        # PLACE WIDGETS TO TOP FRAME
        model_label.grid(row=0, columnspan=3)
        width_label.grid(row=1, column=0)
        length_label.grid(row=1, column=2)
        entry_W.grid(row=1, column=1)
        entry_L.grid(row=1, column=3)

        # ROWCONFIGURE - CENTER
        center.grid_rowconfigure(0, weight=1)
        center.grid_columnconfigure(1, weight=1)
        # CENTER FRAME
        ctr_left = tk.Frame(center, bg='blue', width=100, height=190)
        ctr_mid =  tk.Frame(center, bg='yellow', width=250, height=190, padx=3, pady=3)
        ctr_right = tk.Frame(center, bg='green', width=100, height=190, padx=3, pady=3)

        # PLACE CENTER FRAMES
        ctr_left.grid(row=0, column=0, sticky="ns")

        ctr_mid.grid(row=0, column=1, sticky="nsew")
        ctr_mid.grid_rowconfigure(0, weight=1)
        ctr_mid.grid_columnconfigure(1, weight=1)

        ctr_right.grid(row=0, column=2, sticky="ns")

        # MID COLUMN - GRAPH
        graph = FigureCanvasTkAgg(fig, ctr_mid)
        graph.get_tk_widget().grid(row=0, column=1, sticky="nsew")
        graph.draw()

        # LEFT BUTTON COLUMN
        candle_time = ttk.Label(ctr_left, text='Candle Time')
        candle1H = ttk.Button(ctr_left, text="1 Hour", command=lambda: changeCandleType("1H"))
        candle4H = ttk.Button(ctr_left, text="4 Hours", command=lambda: changeCandleType("4H"))
        candle1D = ttk.Button(ctr_left, text="1 Day", command=lambda: changeCandleType("1D"))
        candle1W = ttk.Button(ctr_left, text="1 Week", command=lambda: changeCandleType("1W"))

        timeSpan = ttk.Label(ctr_left, text='Time Span')
        timeSpan1D = ttk.Button(ctr_left, text="1 Day", command=lambda: controller.show_frame(BTCe_Page))
        timeSpan1W = ttk.Button(ctr_left, text="1 Week", command=lambda: controller.show_frame(BTCe_Page))
        timeSpan1M = ttk.Button(ctr_left, text="4 Weeks", command=lambda: controller.show_frame(BTCe_Page))
        timeSpanFull = ttk.Button(ctr_left, text="Full", command=lambda: controller.show_frame(BTCe_Page))

        candle_time.grid(row=0, columnspan=3,padx=10, pady=10)
        candle1H.grid(row=1, columnspan=3)
        candle4H.grid(row=2, columnspan=3)
        candle1D.grid(row=3, columnspan=3)
        candle1W.grid(row=4, columnspan=3)

        timeSpan.grid(row=6, columnspan=3, padx=10, pady=10)
        timeSpan1D.grid(row=7, columnspan=3)
        timeSpan1W.grid(row=8, columnspan=3)
        timeSpan1M.grid(row=9, columnspan=3)
        timeSpanFull.grid(row=10, columnspan=3)

        # RIGHT BUTTON COLUMN
        tradeBTC_lbl = ttk.Label(ctr_right, text='TRADE')
        buyBTC_btn = ttk.Button(ctr_right, text="BUY BTC", command=lambda: cunt())
        sellBTC_btn = ttk.Button(ctr_right, text="SELL BTC", command=lambda: controller.show_frame(BTCe_Page))
        skip_btn = ttk.Button(ctr_right, text="SKIP", command=lambda: controller.show_frame(BTCe_Page))

        timeSpan = ttk.Label(ctr_right, text='Time Span')
        timeSpan1D = ttk.Button(ctr_right, text="1 Day", command=lambda: controller.show_frame(BTCe_Page))
        timeSpan1W = ttk.Button(ctr_right, text="1 Week", command=lambda: controller.show_frame(BTCe_Page))
        timeSpan1M = ttk.Button(ctr_right, text="4 Weeks", command=lambda: controller.show_frame(BTCe_Page))

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
ani = animation.FuncAnimation(fig, animate, interval=2000)

app.mainloop()



