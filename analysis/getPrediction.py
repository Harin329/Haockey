import pandas as pd
import csv

features = []

with open('data/features.csv', mode ='r') as featureFile:
    featureReader = csv.reader(featureFile)
    for feature in featureReader:
        features.append(feature)

print(features)

df = pd.read_csv("data/current_data.csv")
playerCount = df.shape[0]
playerMap = {}

for feature in features:
    print("==================================" + feature[0] + "====================================")
    start = playerCount
    sorted_df = df.sort_values(by=[feature[0]], ascending=False).loc[:, ["Name", "Position", "Team", feature[0], "upcomingDifficulty"]]
    print(sorted_df.head(10))
    for player in sorted_df.itertuples():
        playerMap[player[1]] = playerMap.get(player[1], 0) + start
        start -= 1

players = sorted(playerMap.items(), key=lambda x: x[1], reverse=True)

with open("data/predictions.csv", "w") as f:
    writer = csv.writer(f)
    for player in players:
        writer.writerow(player)
print("Prediction Results Saved to predictions.csv!")

print("==================================Validation Saving====================================")
sorted_df = df.sort_values(by=["powerPlayGoals_W"], ascending=False).loc[:, ["Name", "Position", "Team", "powerPlayGoals_W", "upcomingDifficulty"]]

with open("data/result_baseline.csv", "a") as f:
    writer = csv.writer(f)
    writer.writerow(['NEW_WEEK'])
    for player in sorted_df.nlargest(10, ['powerPlayGoals_W'], keep='all').itertuples():
        writer.writerow([player[1]])
print("Baseline Results Saved to result_baseline.csv!")

with open("data/result_prediction.csv", "a") as fa:
    writer = csv.writer(fa)
    writer.writerow(['NEW_WEEK'])
    for player in players[:10]:
        writer.writerow([player[0]])
print("Prediction Validation Saved to result_prediction.csv!")