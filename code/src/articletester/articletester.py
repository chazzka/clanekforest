import numpy as np
import matplotlib.pyplot as plt
from itertools import *
from toolz import groupby, unique


# @deprecated, use plotXYWithMean
def plotDataWithMean(xyData):
    # todo: toto lepsi
    yValues = list(map(lambda x: x[1] ,xyData))
    mean = np.mean(yValues)
    grouped = groupby(lambda x: x[1] > mean, xyData)

    print(grouped)
    
    fig = plt.figure()
    ax1 = fig.add_subplot()

    ax1.scatter(*zip(*grouped[True]), c='green')
    ax1.scatter(*zip(*grouped[False]), c='blue')
    ax1.axhline(mean, c='red')
    plt.legend(loc='upper left')
    plt.xlabel("Time")
    plt.ylabel("Observed value")
    plt.show()


def plotXYData(xdata, ydata, fig_ax_tuple, savepath = 0, c='red'):
    print(fig_ax_tuple)
    fig = fig_ax_tuple[0]
    ax = fig_ax_tuple[1]
    ax.scatter(xdata, ydata, c=c)
    plt.xlabel("Time")
    plt.ylabel("Observed value")

    if savepath:
        plt.savefig(savepath, format="svg")

    return fig, ax


def plotYData(yvalue, fig_ax_tuple):
    
    fig = fig_ax_tuple[0]
    ax = fig_ax_tuple[1]
    ax.axhline(yvalue)

    return fig, ax


def plotXYWithMean(trainXyValues, savepath = 0):
    mean = np.mean(list(map(lambda x: x[1] ,trainXyValues)))

    firstFig, firstAx = plotXYData(*zip(*groupby(lambda x: x[1] > mean, trainXyValues)[True]), plt.subplots())
    kombajn, kombajnax = plotXYData(*zip(*groupby(lambda x: x[1] > mean, trainXyValues)[False]), (firstFig, firstAx))
    finalfig, finalax = plotYData(mean, (kombajn, kombajnax))
    if savepath:
        plt.savefig(savepath, format="svg")
    else:
        plt.show()
