import random
from random import randint
import pandas as pd
import numpy as np

class PlayGame(object):
    def __init__(self):
        self.gameIsRunning = True

    def startGame(self):
        print("Game Started")

        self.gameLength = 730
        self.amountToSpend = 500
        self.initialBalance = 5000
        self.cashBalance = 5000
        self.fullBalance = self.cashBalance
        self.prevFullBalance = self.fullBalance
        self.BTC_Balance = 0
        self.currentBTCPrice = 0
        self.initialTimeRange = 730

        dateParse = lambda x: pd.datetime.strptime(x, "%Y-%m-%d %I-%p")
        self.df = pd.read_csv("Gdax_BTCUSD_1h.csv", parse_dates=["Date"], date_parser=dateParse, index_col=0)

        self.startDate, self.endDate, self.startIndex, self.endIndex = self.randomChart()
        self.df_segment = self.df.loc[self.startDate : self.endDate]

        print("c_START:",self.startIndex," - ",self.startDate,"\n","c_END: ",self.endIndex, " - ",self.endDate)

        self.getInitBTCPrice()
        self.rekt = False
        self.done = False
        self.cnt = 1
        self.reward = 0

    def getInitBTCPrice(self):
        endIndex = self.endIndex - 1
        endDate = self.df.index[endIndex]
        nextRow = self.df.loc[[endDate]]
        self.currentBTCPrice = nextRow["Close"][0]

    def randomChart(self):
        hoursIndexCount = len(self.df.index)

        startIndex = randint(1600, hoursIndexCount)
        endIndex = startIndex - self.initialTimeRange

        startDate = self.df.index[startIndex]
        endDate = self.df.index[endIndex - 1]

        startDateStr = startDate.strftime("%Y-%m-%d %H:%M:%S")
        endDateStr = endDate.strftime("%Y-%m-%d %H:%M:%S")

        return startDateStr, endDateStr, startIndex, endIndex

    def nextStep(self, action):
        self.cnt = self.cnt + 1
        # NEXT ROW
        self.endIndex = self.endIndex - 1
        self.endDate = self.df.index[self.endIndex - 1]
        self.nextRow = self.df.loc[[self.endDate]]
        self.df_segment = pd.concat([self.nextRow, self.df_segment])

        self.currentBTCPrice = self.nextRow["Close"][0]

        if action == "Buy BTC":
            if self.amountToSpend > self.cashBalance:   
                self.cashBalance = 0
                self.BTC_Balance = round((self.BTC_Balance + (self.cashBalance / self.currentBTCPrice)), 5)
            else:
                self.cashBalance = self.cashBalance - self.amountToSpend
                self.BTC_Balance = round((self.BTC_Balance + (self.amountToSpend / self.currentBTCPrice)), 5)

        if action == "Sell BTC":
            moneyWorthInBTC = self.amountToSpend / self.currentBTCPrice  # 0.1
            
            if moneyWorthInBTC > self.BTC_Balance:
                self.cashBalance = self.cashBalance + (self.BTC_Balance * self.currentBTCPrice)
                self.BTC_Balance = 0
                print("Money worth is bigger then BTC balance. New Cash Balance: ", self.cashBalance)
            else:
                self.BTC_Balance = self.BTC_Balance - moneyWorthInBTC
                self.cashBalance = self.cashBalance + self.amountToSpend

        self.cashBalance = round((self.cashBalance), 0)
        self.BTC_Balance = round((self.BTC_Balance), 5)
        self.fullBalance = round((self.cashBalance + (self.BTC_Balance * self.currentBTCPrice)), 0)

        if self.fullBalance <= 0:
            self.rekt = True

        if self.cnt == self.gameLength:
            self.done = True

            if (self.fullBalance - self.initialBalance) < 0:
                self.rekt = True

        self.reward = self.fullBalance - self.prevFullBalance
        print("REWARD: ", self.reward)
        self.prevFullBalance = self.fullBalance

        return self.nextRow, self.rekt, self.done, self.reward

    def getChartData(self):
        return self.df_segment




if __name__ == "__main__":
    test = PlayGame()
    test.startGame()
    test.nextStep("Buy BTC")


