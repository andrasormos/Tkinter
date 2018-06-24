import random
from random import randint
import pandas as pd
import numpy as np



startDate = "2018-1-1 01:00:00"
endDate = "2018-2-1 01:00:00"

class PlayGame(object):
    def __init__(self):
        print("Game Began")
        self.max_memory = list()

        dateParse = lambda x: pd.datetime.strptime(x, "%Y-%m-%d %H-%p")
        self.df = pd.read_csv("Gdax_BTCUSD_1h.csv", parse_dates=["Date"], date_parser=dateParse, index_col=0)

        self.randomChart()


    def loadChart(self):
        dateParse = lambda x: pd.datetime.strptime(x, "%Y-%m-%d %H-%p")
        df = pd.read_csv("Gdax_BTCUSD_1h.csv", parse_dates=["Date"], date_parser=dateParse, index_col=0)
        return df

    def randomChart(self):
        hoursCount = len(self.df.index)
        usableCount = hoursCount - 800
        startIndex = randint(0, usableCount)
        endIndex = startIndex - 730

        startDate = self.df.index[startIndex]
        endDate = self.df.index[endIndex]

        print(startDate, " - ", endDate)






    def loadChart(self):
        dateParse = lambda x: pd.datetime.strptime(x, "%Y-%m-%d %H-%p")
        df = pd.read_csv("Gdax_BTCUSD_1h.csv", parse_dates=["Date"], date_parser=dateParse, index_col=0)
        df = df.loc[startDate: endDate]

        # RESAMPLING
        df_ohlc = df["Close"].resample("1H").ohlc()
        df_volume = df["Volume To"].resample("1H").sum()
        #print(df_ohlc.head())

        return df_ohlc, df_volume



if __name__ == "__main__":
    PlayGame()