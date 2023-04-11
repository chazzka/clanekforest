import pickle
import logging




# possible trainXyValues:
# trainXyValues = list(createRandomData()) - make use of mock module
# trainXyValues = list(product(range(100), range(250))) - make fill data
def trainAndPredict(trainXyValues, scikitmodel, args, transformingFun = lambda train, predict: predict):
    #prediction = doTrain(trainXyValues, args, scikitmodel).fit_predict(trainXyValues)
    print(args)
    prediction = scikitmodel(**args).fit_predict(trainXyValues)

    return map(transformingFun, trainXyValues, prediction)



# accept list of tuples (x,y), return predicted array
# returns list[-1=anomalies/1=no anomalies]
def predict(df, savedModel):
    prediction = savedModel.predict(list(df))
    # if observed value was 0.0, assign 1 - no anomaly
    return map(lambda x,y: 1 if x[1] == 0 else y, df, prediction)

def fitPredict(df, model):
    prediction = model.fit_predict(list(df))
    # if observed value was 0.0, assign 1 - no anomaly
    return map(lambda x,y: 1 if x[1] == 0 else y, df, prediction)


def getClusterLabels(xyValues, predicted, clusterArgs, model):
    anomalies = map(lambda x: -x, predicted)
    return model(**clusterArgs).fit_predict(list(xyValues), sample_weight=list(anomalies))


def doTrain(X_train, trainingArgs, model):
    return model(**trainingArgs).fit(X_train)


def saveModel(model, filename):
    logging.info(f"saving model {filename}")
    pickle.dump(model, open(f'models/{filename}', 'wb'))


def loadModel(path):
    return pickle.load(open(path, 'rb'))
