import pandas as pd
import numpy as np
from random import randint
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from GameEngine import PlayGame
import csv


GE = PlayGame()

games = 1
gameLength = 168
initTimerange = 1460
timeStepSize = "H"

actions = ["Skip", "Buy BTC", "Sell BTC"]

x = []
y = []

for game in range(games):
    GE.startGame(gameLength, initTimerange, timeStepSize)
    done = False

    df_segment = GE.getChartData()

    print(df_segment)

    #for step in range(gameLength):
    while done == False:
        action = actions[np.random.choice(np.arange(0, 3), p=[0.9, 0.05, 0.05])]
        nextRow, rekt, done, reward = GE.nextStep(action)

        #print(nextRow)

    if done == True:
        profit = GE.fullBalance - GE.initialBalance
        reward = GE.reward
        print("Game:", game, "Profit:", profit, "Reward:", reward)

        y.append(profit)
        x.append(GE.startDate)
        df = pd.DataFrame({"hours": x, "profits": y})
        df.to_csv("gameLog.csv")



'''
df = pd.DataFrame({ "hours" : x, "profits" : y })
df["hours"] = pd.to_datetime((df["hours"]))
df = df.set_index("hours")

fig, ax = plt.subplots()
ax.plot(df.index, df["profits"], ".", markersize=1 )

ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))

fig.autofmt_xdate()
plt.show()
'''