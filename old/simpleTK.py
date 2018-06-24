#from tkinter import *

import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title('Model Definition')
root.geometry('{}x{}'.format(460, 350))

# create all of the main containers
center = tk.Frame(root, bg='gray2', width=50, height=40, padx=3, pady=3)

# layout all of the main containers
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

center.grid(row=1, sticky="nsew")

# create the center widgets
center.grid_rowconfigure(0, weight=1)
center.grid_columnconfigure(1, weight=1)

ctr_left = tk.Frame(center, bg='blue', width=100, height=190)
ctr_mid = tk.Frame(center, bg='yellow', width=250, height=190, padx=3, pady=3)
ctr_right = tk.Frame(center, bg='green', width=100, height=190, padx=3, pady=3)

ctr_left.grid(row=0, column=0, sticky="ns")
ctr_mid.grid(row=0, column=1, sticky="nsew")
ctr_right.grid(row=0, column=2, sticky="ns")

root.mainloop()