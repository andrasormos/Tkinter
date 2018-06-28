import pandas as pd
import numpy as np
from random import randint
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from GameEngine import PlayGame


GE = PlayGame()

games = 300
gameLength = 168
initTimerange = 1460
timeStepSize = "H"

actions = ["Skip", "Buy BTC", "Sell BTC"]

x = []
y = []

for game in range(games):
    GE.startGame(gameLength, initTimerange, timeStepSize)
    #print(GE.currentBTCPrice)


    for step in range(gameLength):
        pass
        action = actions[randint(0,2)]
        #print("Action:", action)

        nextRow, rekt, done, reward = GE.nextStep(action)
        #print("Next Row:", nextRow, "\n", "Rekt:", rekt, "\n", "Done:", done, "\n", "Reward:", reward)


    profit = GE.fullBalance - GE.initialBalance
    print("Profit:", profit)
    y.append(profit)
    x.append(GE.startDate)
    print("\n")



df = pd.DataFrame({ "hours" : x, "profits" : y })
df["hours"] = pd.to_datetime((df["hours"]))
df = df.set_index("hours")

fig, ax = plt.subplots()
ax.plot(df.index, df["profits"], ".", markersize=1 )

ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))

fig.autofmt_xdate()
plt.show()

'''

x = x.map(mdates.date2num)

fig, ax = plt.subplots()
ax.plot(x,y, ".")

ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))


fig.autofmt_xdate()
plt.show()



plt.plot(x, y, ".", label="First Line")
plt.xlabel("Plot Number")

plt.legend()

plt.show()


# xticks=["2017-1-1 01:00:00","2018-12-1 01:00:00"]

'''