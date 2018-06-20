import tkinter as tk

#   {} - alt + 7
#   [] - alt + 8
#   & - alt + 1
#   # - alt +shift + 3


LARGE_FONT = ("Verdana", 12)

class SeaofBTCapp(tk.Tk): # inherit from the tk class

    def __init__(self, *args, **kwargs ): # ars - any number of variables being passed into here, kwargs - passing dictionaries

        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self) # the actual main window

        container.pack(side= "top", fill="both", expand= True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = { }
        frame = StartPage(container, self)
        self.frames[StartPage] = frame

        frame.grid(row= 0, column= 0, sticky="nsew") # sticky is alignment north south east west, stretch everything to the sides of the window


        self.show_frame(StartPage)

    def show_frame(self,cont): # bings chosen frame to the front
        frame = self.frames[cont]
        frame.tkraise() # bring frame to the front


class StartPage(tk.Frame): # inherit tk.Frame so we dont have to call upon that

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Start Page", font = LARGE_FONT) # this is just an object that we defined, we havent done anything with it yet
        label.pack(pady= 10, padx=10)


app = SeaofBTCapp()
app.mainloop()



