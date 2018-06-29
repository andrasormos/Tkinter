import pandas as pd
import numpy as np
from random import randint
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


df = pd.read_csv("gameLog.csv")

# REMOVE DATE LABELS THATS WHAT CAUSES FREEZE

#ax.plot(df["hours"], df["profits"], ".", markersize=1 )


fig = plt.figure()
plt.title("Game Length & Epsilon")
ax1 = fig.add_subplot(111)


ax1.plot(df["hours"], df["profits"],".", color='r', markersize=0.6)


plt.show()
