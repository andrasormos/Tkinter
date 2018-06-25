import random
from random import randint
import pandas as pd
import numpy as np

#self.startDate = "2018-01-01 01:00:00"
#self.endDate = "2018-01-02 01:00:00"


class PlayGame(object):
    def __init__(self):
        self.gameIsRunning = True

    def startGame(self):
        print("Game Started")
        dateParse = lambda x: pd.datetime.strptime(x, "%Y-%m-%d %I-%p")
        self.df = pd.read_csv("Gdax_BTCUSD_1h.csv", parse_dates=["Date"], date_parser=dateParse, index_col=0)
        self.startDate, self.endDate, self.startIndex, self.endIndex = self.randomChart()
        self.df_segment = self.df.loc[self.startDate : self.endDate]
        print("clss_START:",self.startIndex, " - ", self.startDate, "\n", "clss_END: ", self.endIndex , " - ", self.endDate)

        self.balance = 2000

    def getStartDate(self):
        return self.startDate

    def getEndDate(self):
        return self.endDate


    def randomChart(self):
        hoursIndexCount = len(self.df.index)

        startIndex = randint(1600, hoursIndexCount)
        endIndex = startIndex - 730

        startDate = self.df.index[startIndex]
        endDate = self.df.index[endIndex - 1]

        startDateStr = startDate.strftime("%Y-%m-%d %H:%M:%S")

        endDateStr = endDate.strftime("%Y-%m-%d %H:%M:%S")

        return startDateStr, endDateStr, startIndex, endIndex


    def nextStep(self, action):
        if action == "Buy BTC":
            # REDUCE BALANCE
            self.balance = self.balance - 500

        if action == "Skip":
            pass

        # NEXT DATE AND PRICE
        self.endIndex = self.endIndex - 1
        self.endDate = self.df.index[self.endIndex - 1]
        print("NEXT:", self.endDate)

        #return observation

    def printBalance(self):
        print("BALANCE:",self.balance)






if __name__ == "__main__":
    test = PlayGame()
    test.startGame()
    test.nextStep("Buy BTC")
    test.nextStep("Buy BTC")