import logging
from logging import config
import requests
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
    'ID': '8480800',
    'Name': 'Quinn Hughes',
    'Position': 'D',
    'Team': 'VAN',
    "timeOnIce" : "27:28",
    "assists" : 3,
    "goals" : 0,
    "pim" : 0,
    "shots" : 3,
    "games" : 1,
    "hits" : 0,
    "powerPlayGoals" : 0,
    "powerPlayPoints" : 1,
    "powerPlayTimeOnIce" : "01:12",
    "evenTimeOnIce" : "26:16",
    "penaltyMinutes" : "0",
    "faceOffPct" : 50.0,
    "shotPct" : 0.0,
    "gameWinningGoals" : 0,
    "overTimeGoals" : 0,
    "shortHandedGoals" : 0,
    "shortHandedPoints" : 0,
    "shortHandedTimeOnIce" : "00:00",
    "blocked" : 0,
    "plusMinus" : 0,
    "points" : 3,
    "shifts" : 32,
    "fanPts" : 0,
    'timeOnIce_W': '',
    'assists_W': '',
    'goals_W': '',
    'pim_W': '',
    'shots_W': '',
    'games_W': '',
    'hits_W': '',
    'powerPlayGoals_W': '',
    'powerPlayPoints_W': '',
    'powerPlayTimeOnIce_W': '',
    'evenTimeOnIce_W': '',
    'penaltyMinutes_W': '',
    'faceOffPct_W': '',
    'shotPct_W': '',
    'gameWinningGoals_W': '',
    'overTimeGoals_W': '',
    'shortHandedGoals_W': '',
    'shortHandedPoints_W': '',
    'shortHandedTimeOnIce_W': '',
    'blocked_W': '',
    'plusMinus_W': '',
    'points_W': '',
    'shifts_W': '',
    'fanPts_W': '',
}

def calculateFantasyPoints(player):
    totalPoint = 0
    totalPoint += player['goals'] * 6
    totalPoint += player['assists'] * 4
    totalPoint += player['plusMinus'] * 2
    totalPoint += player['powerPlayGoals'] * 8
    totalPoint += player['powerPlayPoints'] * 2
    totalPoint += player['shortHandedGoals'] * 10
    totalPoint += player['gameWinningGoals'] * 10
    totalPoint += player['shots'] * 1
    totalPoint += player['hits'] * 1
    totalPoint += player['blocked'] * 1
    return totalPoint

# Convert Time String to Seconds
def convertTimeToSeconds(timeString):
    timeList = timeString.split(':')
    return int(timeList[0]) * 60 + int(timeList[1])

def addGame(current, newGameMap):
    for key in newGameMap:
        if key in ['timeOnIce', 'powerPlayTimeOnIce', 'evenTimeOnIce', 'shortHandedTimeOnIce']:
            current[key] = current[key] + convertTimeToSeconds(newGameMap[key])
        elif key in ['shotPct', 'faceOffPct']:
            current[key] = (current[key] + newGameMap[key]) / 2 
        else:
            current[key] = current[key] + int(newGameMap[key])
    current['fanPts'] = current['fanPts'] + calculateFantasyPoints(newGameMap)
    return current

print("==================================Get Data====================================")
# [Stats @ Week X] --> [PPG @ Week X + 1 ]

# Get active NHL players
# playerItem = []

# response = requests.get('https://statsapi.web.nhl.com/api/v1/teams?expand=team.roster')
# res = response.json()

# teams = res['teams']
# for team in teams:
#     print(team['name'])
#     roster = team['roster']['roster']
#     for player in roster:
#         print(player['person']['fullName'])
#         playerItem.append([player['person']['id'], player['person']['fullName'], player['position']['code'], team['abbreviation']])

# with open("players.csv", "w") as f:
#     writer = csv.writer(f)
#     for player in playerItem:
#         writer.writerow(player)
# print("Active players saved to players.csv!")



# For each player, extract format in form of sample data above
df = pd.DataFrame(columns=definitions.keys())
playerID = []
startDate = datetime.datetime(2021, 10, 12)

with open('players.csv', mode ='r') as playersFile:
    reader = csv.reader(playersFile)
    for player in reader:
        if player[2] != 'G':
            playerID.append(player[0])
            response = requests.get('https://statsapi.web.nhl.com/api/v1/people/' + player[0] + '/stats?stats=gameLog&season=20212022')
            res = response.json()

            playerInfo = [player[0], player[1], player[2], player[3]]

            sunday = datetime.datetime(2021, 10, 17)
            
            weekInfo = {
                "timeOnIce" : 0,
                "assists" : 0,
                "goals" : 0,
                "pim" : 0,
                "shots" : 0,
                "games" : 0,
                "hits" : 0,
                "powerPlayGoals" : 0,
                "powerPlayPoints" : 0,
                "powerPlayTimeOnIce" : 0,
                "evenTimeOnIce" : 0,
                "penaltyMinutes" : 0,
                "faceOffPct" : 0,
                "shotPct" : 0,
                "gameWinningGoals" : 0,
                "overTimeGoals" : 0,
                "shortHandedGoals" : 0,
                "shortHandedPoints" : 0,
                "shortHandedTimeOnIce" : 0,
                "blocked" : 0,
                "plusMinus" : 0,
                "points" : 0,
                "shifts" : 0,
                "fanPts" : 0,
            }
            seasonInfo = weekInfo.copy()
            resultPPG = 0

            gameList = list(res['stats'][0]['splits'])
            gameList.reverse()

            for game in gameList:
                if (datetime.datetime.strptime(game['date'], '%Y-%m-%d')) <= sunday:
                    weekInfo = addGame(weekInfo, game['stat'])
                    seasonInfo = addGame(seasonInfo, game['stat'])
                    resultPPG += game['stat']['powerPlayGoals']
                else:
                    print('Write to Week')
                    row = playerInfo + list(seasonInfo.values()) + list(weekInfo.values())
                    df.loc[len(df)] = row
                    # print(row)
                    # print(resultPPG)
                    
                    sunday += datetime.timedelta(days=7)
                    resultPPG = 0
                    weekInfo = {
                        "timeOnIce" : 0,
                        "assists" : 0,
                        "goals" : 0,
                        "pim" : 0,
                        "shots" : 0,
                        "games" : 0,
                        "hits" : 0,
                        "powerPlayGoals" : 0,
                        "powerPlayPoints" : 0,
                        "powerPlayTimeOnIce" : 0,
                        "evenTimeOnIce" : 0,
                        "penaltyMinutes" : 0,
                        "faceOffPct" : 0,
                        "shotPct" : 0,
                        "gameWinningGoals" : 0,
                        "overTimeGoals" : 0,
                        "shortHandedGoals" : 0,
                        "shortHandedPoints" : 0,
                        "shortHandedTimeOnIce" : 0,
                        "blocked" : 0,
                        "plusMinus" : 0,
                        "points" : 0,
                        "shifts" : 0,
                        "fanPts" : 0,
                    }
                    weekInfo = addGame(weekInfo, game['stat'])
                    seasonInfo = addGame(seasonInfo, game['stat'])
                    resultPPG += game['stat']['powerPlayGoals']


print(df.head(100))


# Append processed data into csv file
# with open("stats.csv", "w") as statsFile:
#     writer = csv.writer(statsFile)
#     for player in playerItem:
#         writer.writerow(player)