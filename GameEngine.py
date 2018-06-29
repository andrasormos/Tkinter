
from random import randint
import pandas as pd

class PlayGame(object):
    def __init__(self):
        self.gameIsRunning = True

        # LOAD DATA
        dateParse = lambda x: pd.datetime.strptime(x, "%Y-%m-%d %I-%p")
        self.df = pd.read_csv("Gdax_BTCUSD_1h_priceOnly.csv", parse_dates=["Date"], date_parser=dateParse, index_col=0)

    def startGame(self, gameLength, initTimerange, timeStepSize):
        self.gameLength = gameLength        # How long the game should go on
        self.initialTimeRange = initTimerange  # How many data increment should be shown as history. Could be hours, months
        self.timeStepSize = timeStepSize       # Does nothing atm
        self.amountToSpend = 500    # How much to purchase crypto for
        self.cashBalance = 5000     # Starting Money
        self.BTC_Balance = 0        # BTC to start with

        if self.timeStepSize == "D":
            self.df = self.df.resample("D" ).mean()

        self.dataSize = len(self.df.index)

        # GET RANDOM SEGMENT FROM DATA
        self.startDate, self.endDate, self.startIndex, self.endIndex = self.randomChart()
        self.df_segment = self.df.loc[self.startDate : self.endDate]
        #print("START ID:",self.startIndex," - ",self.startDate,"\n","END ID: ",self.endIndex, " - ",self.endDate)

        self.currentBTCPrice = 0
        self.initialBalance = self.cashBalance
        self.fullBalance = self.cashBalance
        self.prevFullBalance = self.fullBalance
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
        if self.timeStepSize == "H":
            startIndex = randint((self.initialTimeRange + 1), (self.dataSize - 1))

            endIndex = startIndex - self.initialTimeRange

        if self.timeStepSize == "D":
            startIndex = randint(0, (self.dataSize - self.initialTimeRange + 1))
            endIndex = startIndex + self.initialTimeRange

        startDate = self.df.index[startIndex]
        endDate = self.df.index[endIndex - 1]

        if self.timeStepSize == "H":
            startDateStr = startDate.strftime("%Y-%m-%d %H:%M:%S")
            endDateStr = endDate.strftime("%Y-%m-%d %H:%M:%S")

        if self.timeStepSize == "D":
            startDateStr = startDate.strftime("%Y-%m-%d")
            endDateStr = endDate.strftime("%Y-%m-%d")

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
                #print("Money worth is bigger then BTC balance. New Cash Balance: ", self.cashBalance)
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
        #print("REWARD: ", self.reward)
        self.prevFullBalance = self.fullBalance

        return self.nextRow, self.rekt, self.done, self.reward

    def getChartData(self):
        return self.df_segment




if __name__ == "__main__":
    test = PlayGame()
    test.startGame()
    test.nextStep("Buy BTC")


