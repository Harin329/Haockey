import csv
import numpy as np
from library.algorithm import feature_ranking ,fisher_score, reliefF, trace_ratio
from model import getKeys

START_POINT = 6

X = []
y = []
ensembleMap = {}

with open('data.csv', mode ='r') as gamesFile:
    gameReader = csv.reader(gamesFile)
    for game in gameReader:
        X.append(game[4:-1])
        y.append(game[-1])

n_samples, n_features = np.shape(X)
n_labels = np.shape(y)

print(n_samples, n_features)
print(n_labels)

X_train = np.array(X, dtype=float)
y_train = np.array(y, dtype=float)

print("==================================fisher_score====================================")

score = fisher_score(X_train, y_train)

idx = feature_ranking(score)

print(idx)

keys = getKeys()[4:-1]

startPoint = START_POINT
for feature in idx[:5]:
    ensembleMap[keys[feature]] = ensembleMap.get(keys[feature], 0) + startPoint
    startPoint -= 1
    print(keys[feature])

print("==================================reliefF====================================")

score = reliefF(X_train, y_train)

idx = feature_ranking(score)

print(idx)

startPoint = START_POINT
for feature in idx[:5]:
    ensembleMap[keys[feature]] = ensembleMap.get(keys[feature], 0) + startPoint
    startPoint -= 1
    print(keys[feature])

print("==================================trace_ratio====================================")

idx, score, subset = trace_ratio(X_train, y_train, 5)

print(idx)

startPoint = START_POINT
for feature in idx[:5]:
    ensembleMap[keys[feature]] = ensembleMap.get(keys[feature], 0) + startPoint
    startPoint -= 1
    print(keys[feature])

print("==================================ensemble====================================")

print(list(ensembleMap.keys())[:5])
