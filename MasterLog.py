import pandas as pd
import numpy as np
from random import randint
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pylab as pylab

graphEvalGamer = False
if 1 == 0:
    Epoch = 4000
    Xlim = 20000
if 1 == 0:
    Epoch = 5000
    Xlim = 25000
if 1 == 0:
    Epoch = 6000
    Xlim = 31000
if 1 == 2:
    Epoch = 9200
    Xlim = 45000
if 1 == 1:
    Epoch = 19000
    Xlim = 100000

if 1==1:

    # TRAINING LOG
    if 1==1:
        trainLog = pd.read_csv("C:/Users/Treebeard/PycharmProjects/A3C_Keras_FlappyBird/trainingLog.csv", sep=",", index_col=0)

    if 1==2:
        trainLog = pd.read_csv("C:/Users/Treebeard/PycharmProjects/A3C_Keras_FlappyBird//Lab/randomTest/files/TO4.csv", sep=",", index_col=0)

    # ------------------------------------------------------------------------------------------------------
    reward_mean = trainLog.reward_mean
    # ------------------------------------------------------------------------------------------------------
    epsilon = trainLog.epsilon
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


    # PLAY LOG
    if 1==1:
        playLog = pd.read_csv("C:/Users/Treebeard/PycharmProjects/A3C_Keras_FlappyBird/playLog.csv", sep=",", index_col=0)
    if 1==2:
        playLog = pd.read_csv("C:/Users/Treebeard/PycharmProjects/A3C_Keras_FlappyBird/Lab/randomTest/files/PO4.csv", sep=",", index_col=0)

    # ------------------------------------------------------------------------------------------------------
    score = playLog["score"]
    randAction = playLog["random"]
    verySure = playLog["verySureMean"]
    # ------------------------------------------------------------------------------------------------------
    predictedChoice = playLog["predictedChoice"]
    predictedChoice = predictedChoice.str.extract(r'.*?([0.0-9.0]+).*?', expand=True)
    predictedChoice = predictedChoice.astype(float)
    # ------------------------------------------------------------------------------------------------------

    # EVAL GAMER
    if 1==12:
        graphEvalGamer = True
        evalGamer = pd.read_csv("C:/Users/Treebeard/PycharmProjects/A3C_Keras_FlappyBird/evalGamer.csv", sep=",", index_col="model")

        evalGamer = evalGamer.evalScore

    fig = plt.figure()

    # AX 1 - T
    ax1 = fig.add_subplot(321)
    ax1.plot(trainLog.index, reward_mean, ".", color='g', markersize=0.4)
    ax1.set_ylim([0, 20])
    ax1.set_xlim([0, Epoch])
    plt.title("Reward")

    # AX 2 - P
    ax2 = fig.add_subplot(323)
    ax2.plot(playLog.index, score, "-", color='c', linewidth=1)
    z = np.polyfit(playLog.index, score, 1)
    p = np.poly1d(z)
    #pylab.plot(playLog.index, p(playLog.index), "r--", markersize=0.1)
    ax2.set_xlim([0, Xlim])
    #ax2.set_ylim([0, 20])
    plt.title("Score")

    # AX 3 - T
    ax3 = fig.add_subplot(325)
    ax3.plot(trainLog.index, loss, ".", color='r', markersize=0.6)
    ax3.plot(trainLog.index, lrate*1000, ".", color='b', markersize=0.2)
    ax3.set_ylim([0, 1])
    ax3.set_xlim([0, Epoch])
    ax3.plot(trainLog.index, epsilon, "-", color='g', markersize=1.6)
    plt.title("Loss")

    # AX 4 - P
    ax4 = fig.add_subplot(322)
    ax4.plot(playLog.index, randAction, ".", color='c', linewidth=0.5, markersize=0.2)
    ax4.set_xlim([0, Xlim])
    ax4.set_ylim([0, 1.1])
    plt.title("Random Action Taken")

    if graphEvalGamer == False:
        # AX B - P
        ax5 = fig.add_subplot(326)
        ax5.plot(playLog.index, verySure, ".", color='c', linewidth=0.5, markersize=0.2)
        ax5.set_xlim([0, Xlim])
        #ax5.set_ylim([0, 1.1])
        plt.title("Very Sure")


    # AX 5 - P
    ax5 = fig.add_subplot(324)
    ax5.plot(playLog.index, predictedChoice, ".", color='g', markersize=0.4)
    ax5.set_xlim([0, Xlim])
    ax5.set_ylim([0, 1.3])
    plt.title("Chance For A Flap")

    if graphEvalGamer == True:
        # AX 5 - P
        ax5 = fig.add_subplot(326)
        ax5.plot(evalGamer.index, evalGamer, "-", color='g', markersize=0.4)
        ax5.set_xlim([0, Epoch])
        #ax5.set_ylim([0, 2000])
        plt.title("Evaluation Score")


    fig.suptitle('Training Log & PlayLog')  # or plt.suptitle('Main title')
    plt.show()


    #ax1.legend()







