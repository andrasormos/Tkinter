import tkinter as tk
from tkinter import ttk

#   {} - alt + 7
#   [] - alt + 8
#   & - alt + 1
#   # - alt +shift + 3

LARGE_FONT = ("Verdana", 12)

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

        for F in (StartPage, PageOne, PageTwo):
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

        button = ttk.Button(self, text= "Page 1",
                            command= lambda: controller.show_frame(PageOne))
        button.pack()

        button2 = ttk.Button(self, text= "Page 2",
                        command=lambda: controller.show_frame(PageTwo))
        button2.pack()

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


app = SeaofBTCapp()
app.mainloop()



