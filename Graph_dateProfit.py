import pandas as pd
import numpy as np
from random import randint
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


df = pd.read_csv("gameLog.csv", index_col=0)


print(df)



df["hours"] = pd.to_datetime((df["hours"]))
df = df.set_index("hours")


fig, ax = plt.subplots()
ax.plot(df.index, df["profits"], ".", markersize=1 )

ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))

fig.autofmt_xdate()
plt.show()

