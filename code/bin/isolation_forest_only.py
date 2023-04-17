from ai.trainer import trainAndPredict
from mock.randomdatagenerator import createRandomData
import sys
import tomli
from itertools import product

import numpy as np

import matplotlib.pyplot as plt

from sklearn.ensemble import IsolationForest as forest
from sklearn.cluster import DBSCAN as dbscan

from articletester.articletester import *

def getConfigFile(path):
    with open(path, mode="rb") as fp:
        return tomli.load(fp)


if __name__ == "__main__":
    try:
        configFile = sys.argv[1]
    except IndexError:
        configFile = "config.toml"

    config = getConfigFile(configFile)

    # training data
    trainXyValues = list(createRandomData())
    # with fill
    #trainXyValues = list(product(range(100), range(250)))
        
    res = trainAndPredict(trainXyValues, forest, args=config["anomaly"])

    fi, ax = plotXYData(*zip(*trainXyValues), plt.subplots(), c=list(res), savepath="figures/contamination40.svg")
    
    plt.show()


    print("done")
    sys.exit(0)
