import pandas as pd
import numpy as np
from random import randint
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

#df.columns = ["update", "reward_mean", "loss"]

works = pd.read_csv("C:/Users/Treebeard/PycharmProjects/A3C_Keras_FlappyBird/saved_models/working/rewards_2.csv", sep=",", index_col=0)
works.loss = works.loss.str.extract(r'.*?([0.0-9.0]+).*?', expand=True)
works.loss = works.loss.astype(float)

# new = pd.read_csv("C:/Users/Treebeard/PycharmProjects/A3C_Keras_FlappyBird/saved_models/whitened_003/rewards.csv", sep=",", index_col=0)
# new.loss = new.loss.str.extract(r'.*?([0.0-9.0]+).*?', expand=True)
# new.loss = new.loss.astype(float)

new = pd.read_csv("C:/Users/Treebeard/PycharmProjects/A3C_Keras_FlappyBird/rewards.csv", sep=",", index_col=0)
new.loss = new.loss.str.extract(r'.*?([0.0-9.0]+).*?', expand=True)
new.loss = new.loss.astype(float)


fig = plt.figure()
plt.title("Reward Mean & Update")
ax1 = fig.add_subplot(111)
ax1.set_ylim([0,15])
ax1.set_xlim([0,15])
ax1.plot(works["update"], works["reward_mean"],".", color='b', markersize=0.6)

ax2 = fig.add_subplot(111)
ax2.set_ylim([0,15])
ax2.set_xlim([0,30000])
ax2.plot(new["update"], new["reward_mean"],".", color='g', markersize=0.6)


plt.show()








