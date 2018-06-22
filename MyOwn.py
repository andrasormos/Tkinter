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

# THESE ARE DEFAULTS WHICH THE USER CAN CHANGE LATER
exchange = "BTC-e"
DatCounter = 9000  # force an update instead of waiting 30 seconds, counter for that is this
programName = "btce"
resampleSize = "15Min"  # each candle stcik will show 15 minutes change
DataPace = "tick"
candleWidth = 0.008
paneCount = 1
topIndicator = "none"
bottomIndicator = "none"
middleIndicator = "none"
chartLoad = True

darkColor = "#824B4B"
lightColor = "#4B8251"
volumeColor = "#7CA1B4"


def loadChart(run):
    global chartLoad

    if run == "start":
        chartLoad = True

    elif run == "stop":
        chartLoad = False

def changeTimeFrame(tf):
    global DataPace
    global DatCounter
    if tf == "7d" and resampleSize == "1Min":
        popupmsg("Too much data chosen, choose a smaller time frame or higher OHLC interval")
    else:
        DataPace = tf
        DatCounter = 9000

def changeSampleSize(size, width):
    global resampleSize
    global DatCounter
    global candleWidth
    if tf == "7d" and resampleSize == "1Min":
        popupmsg("Too much data chosen, choose a smaller time frame or higher OHLC interval")

    elif DataPace == "tick":
        popupmsg("You're currently viewing tick data, not OHLC")
    else:
        resampleSize = size
        DatCounter = 9000
        candleWidth = width

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
            if exchange == "BTC-e":
                a = plt.subplot2grid((6, 4), (0, 0), rowspan=5, colspan=4)  # 6x4 - (0,0) top left corner, 5 rows and 4 columns, leaving one row remaining
                a2 = plt.subplot2grid((6, 4), (5, 0), rowspan=1, colspan=4, sharex=a)  # shares the x axis with a (affects zooming)

                dataLink = "https://wex.nz/api/3/trades/btc_usd?limit=2000"
                data = urllib.request.urlopen(dataLink)
                data = data.read().decode("utf-8")  # this is in bytes so we have to decode it into strings
                data = json.loads(data)  # read it into strings
                # json is a list of lists, which is a dictionary, the key is BTC and the value is all the trading info
                # but then the value is also a list of lists made of type and others...
                data = data["btc_usd"]
                data = pd.DataFrame(data)  # became a pandas dataset

                data["datestamp"] = np.array(data["timestamp"]).astype("datetime64[s]")
                allDates = data["datestamp"].tolist()  # for volume we need both the sell and buy dates

                buys = data[(data["type"] == "bid")]
                buyDates = (buys["datestamp"]).tolist()

                sells = data[(data["type"] == "ask")]
                sellDates = (sells["datestamp"]).tolist()

                volume = data["amount"]  # its part of the json, has to do with the trading volume

                a.clear()
                a.plot_date(buyDates, buys["price"], lightColor,
                            label="buys")  # X parameter will be dates and the Y will be price
                a.plot_date(sellDates, sells["price"], darkColor, label="sells")

                a2.fill_between(allDates, 0, volume, facecolors=volumeColor)

                a.xaxis.set_major_locator(mticker.MaxNLocator(5))  # making sure dates wont run over each other
                a.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d% %H:M:S"))
                plt.setp(a.get_xticklabels(), visible=False)

                a.legend(bbox_to_anchor=(0, 1.02, 1, .102), loc=3, ncol=2, borderaxespad=0)

                title = "BTC-e BTCUSD Prices\nLast Price: " + str(data["price"][1999])
                a.set_title(title)
                priceData = data["price"].apply(float).tolist()


        except Exception as e:
            print("Failed because of:", e)

        else:
            DatCounter += 1 # INCREMENT COUNTER


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
        exchangeChoice.add_command(label="BTC-e", command=lambda: changeExchange("BTC-e", "btce"))
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

        mainI = tk.Menu(menubar, tearoff=1)
        mainI.add_command(label="None", command=lambda: addMiddleIndicator("none"))
        mainI.add_command(label="SMA", command=lambda: addMiddleIndicator("sma"))
        mainI.add_command(label="EMA", command=lambda: addMiddleIndicator("ema"))
        menubar.add_cascade(label="Main/middle Indicator", menu=mainI)


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
        label = ttk.Label(self, text=("""BAWSAQ CRYPTO trading application
use at your own risk. There it is no promise
of warranty"""), font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Agree", command=lambda: controller.show_frame(BTCe_Page))
        button1.pack()

        button2 = ttk.Button(self, text="Disagree", command=quit)
        button2.pack()

class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text=("Page One"), font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        button1 = ttk.Button(self, text="Back to Home",
                             command=lambda: controller.show_frame(StartPage))
        button1.pack()

class BTCe_Page(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
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


app = SeaofBTCapp()
app.geometry("1280x720")
ani = animation.FuncAnimation(f, animate, interval=2000)
app.mainloop()



