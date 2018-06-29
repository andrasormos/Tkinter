import random
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#dateParse = lambda x: pd.datetime.strptime(x, "%Y-%m-%d %I-%p")
df = pd.read_csv("Gdax_BTCUSD_1h.csv", index_col=0)

df.drop("Symbol", axis=1, inplace=True)
df.drop("Open", axis=1, inplace=True)
df.drop("High", axis=1, inplace=True)
df.drop("Low", axis=1, inplace=True)
df.drop("Volume From", axis=1, inplace=True)
df.drop("Volume To", axis=1, inplace=True)

df.to_csv("Gdax_BTCUSD_1h_PriceOnly.csv", index=True)

print(type(df))