import requests
import csv
import datetime
import pandas as pd
from model import definitions

baseWeekInfo = {
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


# Calculate Matchup Difficulty
def calculateDifficulty(newGame):
    base = 50
    homeTeam = newGame['isHome']
    team = newGame['team']['link']
    opponent = newGame['opponent']['link']

    # Home Advantage
    if homeTeam:
        base = 40
    else:
        base = 60

    responseTeam = requests.get('https://statsapi.web.nhl.com' + team + '?expand=team.stats')
    responseOpp = requests.get('https://statsapi.web.nhl.com' + opponent + '?expand=team.stats')
    resTeam = responseTeam.json()
    resOpp = responseOpp.json()
    statTeam = resTeam['teams'][0]['teamStats'][0]['splits'][0]['stat']
    statOpp = resOpp['teams'][0]['teamStats'][0]['splits'][0]['stat']

    # Team Strength Difference
    evenTeam = statTeam['goalsPerGame'] * 10
    evenOpp = statOpp['goalsAgainstPerGame'] * 10
    base += (evenTeam + evenOpp)

    shotTeam = statTeam['shotsPerGame'] * 5
    shotOpp = statOpp['shotsAllowed'] * 5
    base += (shotTeam + shotOpp)

    # Team Power Play Strength Difference
    percentTeam = float(statTeam['powerPlayPercentage'])
    percentOpp = float(statTeam['penaltyKillPercentage'])
    base += (percentTeam + (100 - percentOpp))

    ppTeam = statTeam['powerPlayGoals'] * 10
    ppOpp = statOpp['powerPlayGoalsAgainst'] * 10
    base += (ppTeam + ppOpp)

    return base

# Create a Game Data Point
def addGame(current, newGame, type):
    newGameMap = newGame['stat']
    for key in newGameMap:
        if key in ['timeOnIce', 'powerPlayTimeOnIce', 'evenTimeOnIce', 'shortHandedTimeOnIce']:
            current[key] = current[key] + convertTimeToSeconds(newGameMap[key])
        elif key in ['shotPct', 'faceOffPct']:
            current[key] = (current[key] + newGameMap[key]) / 2 
        else:
            current[key] = current[key] + int(newGameMap[key])
    current['fanPts'] = current['fanPts'] + calculateFantasyPoints(newGameMap)
    if (type == 'W'):
        current['upcomingDifficulty'] = (current['upcomingDifficulty'] + calculateDifficulty(newGame)) / 2
    return current

print("==================================Get Data====================================")
# [Stats @ Week X] --> [PPG @ Week X + 1 ]

# Get active NHL players
playerItem = []

response = requests.get('https://statsapi.web.nhl.com/api/v1/teams?expand=team.roster')
res = response.json()

teams = res['teams']
for team in teams:
    print(team['name'])
    roster = team['roster']['roster']
    for player in roster:
        print(player['person']['fullName'])
        playerItem.append([player['person']['id'], player['person']['fullName'], player['position']['code'], team['abbreviation']])

with open("players.csv", "w") as f:
    writer = csv.writer(f)
    for player in playerItem:
        writer.writerow(player)
print("Active players saved to players.csv!")



# For each player, extract format in form of sample data above
df = pd.DataFrame(columns=definitions.keys())
playerID = []
startDate = datetime.datetime(2021, 10, 12)

with open('players.csv', mode ='r') as playersFile:
    playerReader = csv.reader(playersFile)
    for player in playerReader:
        if player[2] != 'G':
            print("Parsing player: " + player[1])
            playerID.append(player[0])
            response = requests.get('https://statsapi.web.nhl.com/api/v1/people/' + player[0] + '/stats?stats=gameLog&season=20212022')
            res = response.json()

            playerInfo = [player[0], player[1], player[2], player[3]]

            sunday = datetime.datetime(2021, 10, 17)
            
            weekInfo = baseWeekInfo.copy()
            weekInfo['upcomingDifficulty'] = 0
            seasonInfo = baseWeekInfo.copy()
            lastWeek = None
            resultPPG = 0


            gameList = list(res['stats'][0]['splits'])
            gameList.reverse()

            for game in gameList:
                if (datetime.datetime.strptime(game['date'], '%Y-%m-%d')) <= sunday:
                    weekInfo = addGame(weekInfo, game, 'W')
                    seasonInfo = addGame(seasonInfo, game, 'S')
                    resultPPG += game['stat']['powerPlayGoals']
                else:
                    if (lastWeek != None):
                        # print('Write to Week: ' + str(sunday))
                        df.loc[len(df)] = lastWeek + [resultPPG]

                    row = playerInfo + list(seasonInfo.values()) + list(weekInfo.values())
                    lastWeek = row
                    
                    sunday += datetime.timedelta(days=7)
                    resultPPG = 0
                    weekInfo = baseWeekInfo.copy()
                    weekInfo['upcomingDifficulty'] = 0
                    weekInfo = addGame(weekInfo, game, 'W')
                    seasonInfo = addGame(seasonInfo, game, 'S')
                    resultPPG += game['stat']['powerPlayGoals']

print(df.head(10))
df.to_csv('data.csv', index=False)
print("Data saved to data.csv!")
