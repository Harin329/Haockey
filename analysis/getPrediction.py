import pandas as pd
import csv

features = [
    "powerPlayTimeOnIce_W",
    "powerPlayGoals",
    "powerPlayTimeOnIce",
    "goals",
    "powerPlayPoints",
    "timeOnIce",
    "evenTimeOnIce",
    "timeOnIce_W",
    "evenTimeOnIce_W",
    "pim_W",
    "goals_W",
    "games",
    "hits",
    "games_W",
    "assists_W",
    "shifts_W",
]

print(features)

df = pd.read_csv("data/current_data.csv")
playerCount = df.shape[0]
playerMap = {}

for feature in features:
    print("==================================" + feature + "====================================")
    start = playerCount
    sorted_df = df.sort_values(by=[feature], ascending=False).loc[:, ["Name", "Position", "Team", feature, "upcomingDifficulty"]]
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