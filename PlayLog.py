import pandas as pd
import numpy as np
from random import randint
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pylab as pylab


# CURRENT PLAYLOG
if 1==1:
    playLog = pd.read_csv("C:/Users/Treebeard/PycharmProjects/A3C_Keras_FlappyBird/playLog.csv", sep=",", index_col=0)
# OLDER PLAYLOG
if 1==2:
    playLog = pd.read_csv("C:/Users/Treebeard/PycharmProjects/A3C_Keras_FlappyBird/Lab/randomTest/files/PO4.csv", sep=",", index_col=0)

score = playLog["score"]
epsilon = playLog["epsilon"]
randAction = playLog["random"]

predictedChoice = playLog["predictedChoice"]
predictedChoice = predictedChoice.str.extract(r'.*?([0.0-9.0]+).*?', expand=True)
predictedChoice = predictedChoice.astype(float)

#Xlim = 100000
Xlim= 10000

fig = plt.figure()

# AX 1
ax1 = fig.add_subplot(221)
ax1.plot(playLog.index, score, "-", color='c', linewidth=1)
z = np.polyfit(playLog.index, score, 1)
p = np.poly1d(z)
#pylab.plot(playLog.index, p(playLog.index), "r--", markersize=0.1)
ax1.set_xlim([0, Xlim])
#ax1.set_ylim([0, 20])
plt.title("Score")

# AX 2
ax2 = fig.add_subplot(222)
ax2.plot(playLog.index, epsilon, ".", color='g', markersize=1.6)
ax2.set_ylim([0, 1.1])
ax2.set_xlim([0, Xlim])
plt.title("Epsilon")

# AX 3
ax3 = fig.add_subplot(223)
ax3.plot(playLog.index, randAction, "-", color='c', linewidth=0.5)
ax3.set_xlim([0, Xlim])
ax3.set_ylim([0, 1.1])
plt.title("Random Action Taken")

# AX 4
ax4 = fig.add_subplot(224)
ax4.plot(playLog.index, predictedChoice, ".", color='g', markersize=0.4)
ax4.set_xlim([0, Xlim])
ax4.set_ylim([0, 1.3])
plt.title("Chance For A Flap")

ax1.legend()

fig.suptitle('Play Log - New Flappy Setup')

plt.show()

