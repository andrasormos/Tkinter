import pandas as pd
import numpy as np
from random import randint
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pylab as pylab

# ax1.set_ylim([0,15])
# ax1.set_xlim([0,30000])

# CURRENT LOG
if 1==1:
    playLog = pd.read_csv("C:/Users/Treebeard/PycharmProjects/A3C_Keras_FlappyBird/playLog.csv", sep=",", index_col=0)
    trainLog = pd.read_csv("C:/Users/Treebeard/PycharmProjects/A3C_Keras_FlappyBird/trainingLog.csv", sep=",", index_col=0)

# CURRENT LOG
if 1==0:
    playLog = pd.read_csv("C:/Users/Treebeard/PycharmProjects/A3C_Keras_FlappyBird/Lab/Log003/playLog.csv", sep=",", index_col=0)
    trainLog = pd.read_csv("C:/Users/Treebeard/PycharmProjects/A3C_Keras_FlappyBird/Lab/Log003/trainingLog.csv", sep=",", index_col=0)

reward = playLog["reward"]
act = playLog["action"]
prof = playLog["profit"]
mean_profit = np.mean(playLog["profit"])
print("mean profit:", mean_profit)

reward_mean = trainLog.reward_mean
trainLog.loss = trainLog.loss.str.extract(r'.*?([0.0-9.0]+).*?', expand=True)
trainLog.loss = trainLog.loss.astype(float)
loss = trainLog.loss
lrate = trainLog.lrate


fig = plt.figure()

# AX 1
ax1 = fig.add_subplot(221)
ax1.plot(playLog.index, reward, ".", color='c', markersize=1.6)
z = np.polyfit(playLog.index, reward, 1)
p = np.poly1d(z)
#pylab.plot(playLog.index, p(playLog.index), "r--", markersize=0.1)
plt.title("Reward")

# AX 2
ax2 = fig.add_subplot(222)
ax2.plot(playLog.index, prof, ".", color='g', markersize=1.6)
z = np.polyfit(playLog.index, prof, 1)
p = np.poly1d(z)
#pylab.plot(playLog.index, p(playLog.index), "r--")
plt.title("Profit")

# AX 3
ax2 = fig.add_subplot(224)
ax2.plot(playLog.index, act, ".", color='b', markersize=1.6)
z = np.polyfit(playLog.index, act, 1)
p = np.poly1d(z)
#pylab.plot(playLog.index, p(playLog.index), "r--")
plt.title("Action")

# AX 4
ax10 = fig.add_subplot(223)
ax10.plot(trainLog.index, reward_mean, ".", color='g', markersize=0.6)
ax10.plot(trainLog.index, trainLog.loss*10, ".", color='r', markersize=0.6)
#ax10.plot(trainLog.index, lrate, ".", color='b', markersize=0.6)
#ax3 = ax1.twinx()
#ax3.plot(trainLog.index, lrate, ".", color='b', markersize=0.6)
ax10.set_ylim([0, 60])

ax1.legend()
ax10.legend()
plt.title("Loss & Reward Mean")


plt.show()


# LAB

# Log 001 - Original Settings
# Init:     84 hours
# Length :  84 hours
# r_t 0.1:  if profit > 0
# r_t 1.5:  if profit > 1000
# r_t -1 :  if profit > -1000

# Log 002 - Increased CNN network values
# Init:     84 hours
# Length:   84 hours
# r_t 0.1:  if profit > 0
# r_t 1.5:  if profit > 5000
# r_t -1 :  if profit > -5000


# To Do
# Increase the sample of data that the network is learning from, as atm it's just 40 hours