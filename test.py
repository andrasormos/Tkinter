import pandas as pd
import numpy as np



dateParse = lambda x: pd.datetime.strptime(x, "%Y-%m-%d %H-%p")
df = pd.read_csv("Gdax_BTCUSD_1h.csv", parse_dates=["Date"], date_parser=dateParse, index_col=0)


#df = pd.read_csv("Gdax_BTCUSD_1h.csv", index_col=0)


#print(df.head())

#print("\n")

#print(df.index[5])

print(df.head())