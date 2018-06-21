import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
import urllib
import json
import pandas as pd
import numpy as np


#   {} - alt + 7
#   [] - alt + 8
#   & - alt + 1
#   # - alt +shift + 3
#   \ - alt + ü
#   > < - alt + shift + Y    or X but that kills window<

LARGE_FONT = ("Verdana", 12)
style.use("ggplot")

f = Figure(figsize=(5, 5), dpi=100)
a = f.add_subplot(111)

def animate(i):
    dataLink = "https://wex.nz/api/3/trades/btc_usd?limit=2000"
    data = urllib.request.urlopen(dataLink)
    data = data.read().decode("utf-8") # this is in bytes so we have to decode it into strings
    data = json.loads(data) # read it into strings,
    # json is a list of lists, which is a dictionary, the key is BTC and the value is all the trading info
    # but then the value is also a list of lists made of type and others...

    data = data["btc_usd"]
    data = pd.DataFrame(data) # became a pandas dataset

    buys = data[ ( data["type"] == "bid" ) ]
    buys["datestamp"] = np.array(buys[ "timestamp" ] ).astype("datetime64[s]") # adding a new column called datestamp with converted time
    buyDates = (buys["datestamp"]).tolist()

    sells = data[ ( data["type"] == "ask" ) ]
    sells["datestamp"] = np.array(sells[ "timestamp" ] ).astype("datetime64[s]") # adding a new column called datestamp
    sellDates = (sells["datestamp"]).tolist()

    a.clear()
    a.plot_date(buyDates, buys["price"]) # X parameter will be dates and the Y will be price
    a.plot_date(sellDates, sells["price"])


class SeaofBTCapp(tk.Tk): # inherit from the tk class
    def __init__(self, *args, **kwargs ): # ars - any number of variables being passed into here, kwargs - passing dictionaries
        tk.Tk.__init__(self, *args, **kwargs)

        #tk.TK.iconbitmap(self, default="icon_Name.ico")
        tk.Tk.wm_title(self, "BAWSAQ")

        container = tk.Frame(self) # the actual main windo
        container.pack(side= "top", fill="both", expand= True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = { }

        for F in (StartPage, BTCe_Page):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row= 0, column= 0, sticky="nsew") # sticky is alignment north south east west, stretch everything to the sides of the window

        self.show_frame(StartPage)

    def show_frame(self,cont): # bings chosen frame to the front
        frame = self.frames[cont]
        frame.tkraise() # bring frame to the front


class StartPage(tk.Frame): # inherit tk.Frame so we dont have to call upon that
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = ttk.Label(self, text=("""BAWSAQ CRYPTO trading application
use at your own risk. There it is no promise
of warranty"""),font=LARGE_FONT)
        label.pack(pady= 10, padx=10)

        button1 = ttk.Button(self, text= "Agree",
                            command= lambda: controller.show_frame(BTCe_Page))
        button1.pack()

        button2 = ttk.Button(self, text= "Disagree",
                        command=quit)
        button2.pack()

class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text=("Page One"),font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        button1 = ttk.Button(self, text= "Back to Home",
                        command=lambda: controller.show_frame(StartPage))
        button1.pack()


class BTCe_Page(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Graph Page",
                         font=LARGE_FONT)  # this is just an object that we defined, we havent done anything with it yet
        label.pack(pady=10, padx=10)
        button1 = ttk.Button(self, text= "Back to Home",
                        command=lambda: controller.show_frame(StartPage))
        button1.pack()

        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side= tk.BOTTOM, fill= tk.BOTH, expand= True)

        toolbar = NavigationToolbar2TkAgg(canvas, self) # we are sending the toolbar to the canvas
        toolbar.update()
        canvas._tkcanvas.pack(side= tk.TOP, fill= tk.BOTH, expand= True)


app = SeaofBTCapp()
ani = animation.FuncAnimation(f, animate, interval=1000)
app.mainloop()



