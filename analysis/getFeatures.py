import csv
import numpy as np
from library.algorithm import feature_ranking ,fisher_score, reliefF, trace_ratio
from model import getKeys

START_POINT = 6

X = []
y = []
ensembleMap = {}

with open('data/data.csv', mode ='r') as gamesFile:
    gameReader = csv.reader(gamesFile)
    for game in gameReader:
        if (game[0] != 'ID'):
            X.append(game[4:-1])
            y.append(game[-1])

n_samples, n_features = np.shape(X)
n_labels = np.shape(y)

print(n_samples, n_features)
print(n_labels)

X_train = np.array(X, dtype=float)
y_train = np.array(y, dtype=float)

keys = getKeys()[4:-1]

print("==================================fisher_score====================================")

score = fisher_score(X_train, y_train)

idx = feature_ranking(score)

print(idx)

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

print("==================================BorutaPy====================================")

from sklearn.ensemble import RandomForestClassifier
from boruta import BorutaPy

rf = RandomForestClassifier(n_jobs=-1, max_depth=24, n_estimators=1000)
rf.fit(X_train, y_train)

iterMap = {}

for i in range(100):
    feat_selector = BorutaPy(rf, n_estimators='auto', two_step=False, verbose=0, random_state=i)
    feat_selector.fit(X_train, y_train)

    idx = feat_selector.ranking_

    for feature in idx[:5]:
        iterMap[keys[feature]] = iterMap.get(keys[feature], 0) + 1

idx = sorted(iterMap.items(), key=lambda x: x[1], reverse=True)

startPoint = START_POINT
for feature in idx[:5]:
    ensembleMap[feature[0]] = ensembleMap.get(feature[0], 0) + startPoint
    startPoint -= 1
    print(feature[0])

print("==================================scikit-rebate====================================")

from skrebate import ReliefF

fs = ReliefF(n_features_to_select=5, n_neighbors=100)
fs.fit(X_train, y_train)

rebateMap = {}
for feature_name, feature_score in zip(keys, fs.feature_importances_):
    # print(feature_name, '\t', feature_score)
    rebateMap[feature_name] = feature_score

idx = sorted(rebateMap.items(), key=lambda x: x[1], reverse=True)

startPoint = START_POINT
for feature in idx[:5]:
    ensembleMap[feature[0]] = ensembleMap.get(feature[0], 0) + startPoint
    startPoint -= 1
    print(feature[0])

print("==================================ensemble====================================")

print(list(ensembleMap.keys()))