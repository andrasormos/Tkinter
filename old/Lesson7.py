import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style

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
    pullData = open("sampleData.txt","r").read()
    dataList = pullData.split("\n")
    xList = []
    yList = []
    for eachLine in dataList:
        if len(eachLine) > 1:
            x, y = eachLine.split(",")
            xList.append(int(x))
            yList.append(int(y))
    a.clear()
    a.plot(xList, yList)


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

        for F in (StartPage, PageOne, PageTwo, PageThree):
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
        label = ttk.Label(self, text="Start Page", font = LARGE_FONT) # this is just an object that we defined, we havent done anything with it yet
        label.pack(pady= 10, padx=10)

        button1 = ttk.Button(self, text= "Page 1",
                            command= lambda: controller.show_frame(PageOne))
        button1.pack()

        button2 = ttk.Button(self, text= "Page 2",
                        command=lambda: controller.show_frame(PageTwo))
        button2.pack()

        button3 = ttk.Button(self, text= "Graph Page",
                        command=lambda: controller.show_frame(PageThree))
        button3.pack()

class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Page One",
                         font=LARGE_FONT)  # this is just an object that we defined, we havent done anything with it yet
        label.pack(pady=10, padx=10)
        button1 = ttk.Button(self, text= "Back to Home",
                        command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = ttk.Button(self, text= "Page 2",
                        command=lambda: controller.show_frame(PageTwo))
        button2.pack()

class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Page Two",
                         font=LARGE_FONT)  # this is just an object that we defined, we havent done anything with it yet
        label.pack(pady=10, padx=10)
        button1 = ttk.Button(self, text= "Back to Home",
                        command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = ttk.Button(self, text= "Page 1",
                        command=lambda: controller.show_frame(PageOne))
        button2.pack()

class PageThree(tk.Frame):

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



