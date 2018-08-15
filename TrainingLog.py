import pandas as pd
import numpy as np
from random import randint
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pylab as pylab



if 1==1:
# TRAINING LOG

    if 1==1:
        trainLog = pd.read_csv("C:/Users/Treebeard/PycharmProjects/A3C_Keras_FlappyBird/trainingLog.csv", sep=",", index_col=0)

    if 1==2:
        trainLog = pd.read_csv("C:/Users/Treebeard/PycharmProjects/A3C_Keras_FlappyBird//Lab/randomTest/files/TO4.csv", sep=",", index_col=0)

    #Epoch = 20000
    Epoch = 3000

    # ------------------------------------------------------------------------------------------------------
    reward_mean = trainLog.reward_mean
    # ------------------------------------------------------------------------------------------------------
    lrate = trainLog.lrate
    # ------------------------------------------------------------------------------------------------------
    trainLog.loss = trainLog.loss.str.extract(r'.*?([0.0-9.0]+).*?', expand=True)
    trainLog.loss = trainLog.loss.astype(float)
    loss = trainLog.loss
    # ------------------------------------------------------------------------------------------------------
    trainLog.policy_loss = trainLog.policy_loss.str.extract(r'.*?([0.0-9.0]+).*?', expand=True)
    trainLog.policy_loss = trainLog.policy_loss.astype(float)
    policy_loss = trainLog.policy_loss.astype(float)
    # ------------------------------------------------------------------------------------------------------
    trainLog.critic_loss = trainLog.critic_loss.str.extract(r'.*?([0.0-9.0]+).*?', expand=True)
    trainLog.critic_loss = trainLog.critic_loss.astype(float)
    critic_loss = trainLog.critic_loss.astype(float)
    # ------------------------------------------------------------------------------------------------------








    fig = plt.figure()

    ax1 = fig.add_subplot(321)
    ax1.plot(trainLog.index, reward_mean, ".", color='g', markersize=0.2)
    ax1.set_ylim([0, 20])
    ax1.set_xlim([0, Epoch])
    plt.title("Reward")

    ax2 = fig.add_subplot(322)
    ax2.plot(trainLog.index, lrate, ".", color='b', markersize=0.2)
    ax2.set_ylim([0, 0.001])
    ax2.set_xlim([0, Epoch])
    plt.title("Lrate")

    ax3 = fig.add_subplot(323)
    ax3.plot(trainLog.index, loss, ".", color='r', markersize=0.2)
    ax3.set_ylim([0, 1])
    ax3.set_xlim([0, Epoch])
    plt.title("Loss")

    ax4 = fig.add_subplot(324)
    ax4.plot(trainLog.index, policy_loss, ".", color='r', markersize=0.2)
    ax4.set_ylim([0, 0.5])
    ax4.set_xlim([0, Epoch])
    plt.title("Policy Loss")

    ax5 = fig.add_subplot(325)
    ax5.plot(trainLog.index, critic_loss, ".", color='r', markersize=0.2)
    ax5.set_ylim([0, 1])
    ax5.set_xlim([0, Epoch])
    plt.title("Critic Loss")

    fig.suptitle('Training Log & PlayLog') # or plt.suptitle('Main title')

    ax1.legend()
    plt.show()





