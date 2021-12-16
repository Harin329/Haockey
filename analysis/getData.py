import logging
from logging import config
from yahoo_oauth import OAuth2
import yahoo_fantasy_api as yfa
import time
import csv
from csv import reader
import datetime
from datetime import timedelta
import matplotlib.pyplot as plt
import pandas as pd

sc = OAuth2(None, None, from_file='../auth/auth.json')

gm = yfa.Game(sc, 'nhl')
league = yfa.League(sc, '411.l.96677')
team = yfa.Team(sc, '411.l.96677.t.2')

definitions = {
    'ID': 'ID',
    'Name': 'Name',
    'Position': 'Position',
    'GP': 'Games Played',
    'G': 'Goals',
    'A': 'Assists',
    'PTS': 'Points',
    '+/-': 'Plus/Minus',
    'PIM': 'Penalty Minutes',
    'PPG': 'Power Play Goals',
    'PPA': 'Power Play Assists',
    'PPP': 'Power Play Points',
    'SHG': 'Short Handed Goals',
    'GWG': 'Game Winning Goals',
    'SOG': 'Shots On Goal',
    'S%': 'Shooting Percentage',
    'HIT': 'Hits',
    'BLK': 'Blocks',
    'PPT': 'Power Play Time',
    'Avg-PPT': 'Average Power Play Time',
    'SHT': 'Short Handed Time',
    'Avg-SHT': 'Average Short Handed Time',
    'COR': 'Corsi',
    'FEN': 'Fenwick',
    'Off-ZS': 'Offensive Zone Starts',
    'Def-ZS': 'Defense Zone Starts',
    'ZS-Pct': 'Zone Start Percentage',
    'GStr': 'Game Star',
    'Shifts': 'Shifts',
    'FP': 'Fan Points',
    'GP_W': 'Games Played This Week',
    'G_W': 'Goals This Week',
    'A_W': 'Assists This Week',
    'PTS_W': 'Points This Week',
    '+/-_W': 'Plus/Minus This Week',
    'PIM_W': 'Penalty Minutes This Week',
    'PPG_W': 'Power Play Goals This Week',
    'PPA_W': 'Power Play Assists This Week',
    'PPP_W': 'Power Play Points This Week',
    'SHG_W': 'Short Handed Goals This Week',
    'GWG_W': 'Game Winning Goals This Week',
    'SOG_W': 'Shots On Goal This Week',
    'S%_W': 'Shooting Percentage This Week',
    'HIT_W': 'Hits This Week',
    'BLK_W': 'Blocks This Week',
    'PPT_W': 'Power Play Time This Week',
    'Avg-PPT_W': 'Average Power Play Time This Week',
    'SHT_W': 'Short Handed Time This Week',
    'Avg-SHT_W': 'Average Short Handed Time This Week',
    'COR_W': 'Corsi This Week',
    'FEN_W': 'Fenwick This Week',
    'Off-ZS_W': 'Offensive Zone Starts This Week',
    'Def-ZS_W': 'Defense Zone Starts This Week',
    'ZS-Pct_W': 'Zone Start Percentage This Week',
    'GStr_W': 'Game Star This Week',
    'Shifts_W': 'Shifts This Week',
    'FP_W': 'Fan Points This Week',
    # 'Team': 'Team',
}

def calculateFantasyPoints(player):
    if player['GP'] == '-' or player['position_type'] == 'G':
        return 0
    totalPoint = 0
    totalPoint += player['G'] * 6
    totalPoint += player['A'] * 4
    totalPoint += player['+/-'] * 2
    totalPoint += player['PPG'] * 8
    totalPoint += player['PPP'] * 2
    totalPoint += player['SHG'] * 10
    totalPoint += player['GWG'] * 10
    totalPoint += player['SOG'] * 1
    totalPoint += player['HIT'] * 1
    totalPoint += player['BLK'] * 1
    return totalPoint

print("==================================Get Data====================================")
# [Stats @ Week X] --> [PPG @ Week X + 1 ]

# Get top 250 NHL players
# playerItem = []

# for page in range(10):
#     url = "https://fantasysports.yahooapis.com/fantasy/v2/league/411.l.96677/players;start=" + str(page * 25) + ";sort=PTS;count=25"
#     response = sc.session.get(url, params={'format': 'json'})
#     res = response.json()

#     players = list(res['fantasy_content']['league'][1]['players'].values())
#     for player in players[:-1]:
#         playerItem.append([player['player'][0][1]['player_id'], player['player'][0][2]['name']['full']])

# with open("players.csv", "w") as f:
#     writer = csv.writer(f)
#     for player in playerItem:
#         writer.writerow(player)
# print("Top 250 players saved to players.csv!")


# For each player, extract format in form of sample data above
playerID = []
startDate = datetime.datetime(2021, 10, 12)

with open('players.csv', mode ='r') as playersFile:
  reader = csv.reader(playersFile)
  for player in reader:
        playerID.append(player[0])

# {'player_id': 7904, 'name': 'Filip Zadina', 'position_type': 'P', 'GP': 29.0, 'G': 4.0, 'A': 6.0, 'PTS': 10.0, '+/-': -7.0, 'PIM': 4.0, 'PPG': 2.0, 'PPA': 2.0, 'PPP': 4.0, 'SHG': 0.0, 'GWG': 1.0, 'SOG': 70.0, 'S%': 0.057, 'HIT': 19.0, 'BLK': 17.0, 'PPT': 3389.0, 'Avg-PPT': 117.0, 'SHT': 3.0, 'Avg-SHT': 0.0, 'COR': 3.0, 'FEN': 14.0, 'Off-ZS': 138.0, 'Def-ZS': 98.0, 'ZS-Pct': 58.47, 'GStr': 0.0, 'Shifts': 498.0}
# {'player_id': 7904, 'name': 'Filip Zadina', 'position_type': 'P', 'GP': '-', 'G': '-', 'A': '-', 'PTS': '-', '+/-': '-', 'PIM': '-', 'PPG': '-', 'PPA': '-', 'PPP': '-', 'SHG': '-', 'GWG': '-', 'SOG': '-', 'S%': '-', 'HIT': '-', 'BLK': '-'}

df = pd.DataFrame(columns=definitions.keys())

stats = league.player_stats(playerID, 'season')
weeklyStats = league.player_stats(playerID, 'date', startDate)
print(weeklyStats)

# for index, id in enumerate(playerID):
#     player = stats[index]
#     weeklyPlayer = weeklyStats[index]
#     if (player['position_type'] != 'G'):
#         seasonList = list(player.values())
#         seasonFan = [calculateFantasyPoints(player)]
#         weekList = list(weeklyPlayer.values())[3:]
#         weekFan = [calculateFantasyPoints(weeklyPlayer)]
#         finalList = seasonList + seasonFan + weekList + weekFan
#         print(len(finalList))
#         print(len(seasonFan))
#         print(len(weekList))
#         print(len(weekFan))
#         df.loc[id, :] = finalList
# print(df)

# resultList = []
    
# start = datetime.datetime(2021, 10, 12)
# sunday = datetime.datetime(2021, 10, 17)
# end = datetime.datetime.now()

# while start <= end:
#     start += timedelta(days=1)
#     print(start)


# Append processed data into csv file
# with open("stats.csv", "w") as statsFile:
#     writer = csv.writer(statsFile)
#     for player in playerItem:
#         writer.writerow(player)