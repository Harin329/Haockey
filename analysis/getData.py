import requests
import csv
import datetime
import pandas as pd
from model import definitions, baseWeekInfo, current

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
def calculateDifficulty(newGame, playerTeam):
    base = 0
    homeTeam = newGame['home']['team']['id'] == playerTeam
    team = None
    opponent = None

    # Home Advantage
    if homeTeam:
        base = 100
        team = newGame['home']['team']['link']
        opponent = newGame['away']['team']['link']
    else:
        base = 70
        team = newGame['away']['team']['link']
        opponent = newGame['home']['team']['link']

    responseTeam = requests.get('https://statsapi.web.nhl.com' + team + '?expand=team.stats')
    responseOpp = requests.get('https://statsapi.web.nhl.com' + opponent + '?expand=team.stats')
    resTeam = responseTeam.json()
    resOpp = responseOpp.json()
    statTeam = resTeam['teams'][0]['teamStats'][0]['splits'][0]['stat']
    statOpp = resOpp['teams'][0]['teamStats'][0]['splits'][0]['stat']

    # Team Strength Difference
    evenTeam = statTeam['goalsPerGame'] * 1
    evenOpp = statOpp['goalsAgainstPerGame'] * 1
    base += (evenTeam + evenOpp)

    shotTeam = statTeam['shotsPerGame'] * 1
    shotOpp = statOpp['shotsAllowed'] * 1
    base += (shotTeam + shotOpp)

    # Team Power Play Strength Difference
    percentTeam = float(statTeam['powerPlayPercentage'])
    percentOpp = float(statTeam['penaltyKillPercentage'])
    base += (percentTeam + (100 - percentOpp))

    ppTeam = statTeam['powerPlayGoals'] * 2
    ppOpp = statOpp['powerPlayGoalsAgainst'] * 2
    base += (ppTeam + ppOpp)

    return base

# Create a Game Data Point
def addGame(current, newGame):
    newGameMap = newGame['stat']
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

with open("data/players.csv", "w") as f:
    writer = csv.writer(f)
    for player in playerItem:
        writer.writerow(player)
print("Active players saved to players.csv!")



# For each player, extract format in form of sample data above
df = pd.DataFrame(columns=definitions.keys())
current_df = pd.DataFrame(columns=current.keys())
startDate = datetime.datetime(2021, 10, 12)

today = datetime.datetime.today()
endDate = today - datetime.timedelta(days=today.weekday()) - datetime.timedelta(hours=today.hour) - datetime.timedelta(minutes=today.minute) - datetime.timedelta(seconds=today.second) - datetime.timedelta(microseconds=today.microsecond)

with open('data/players.csv', mode ='r') as playersFile:
    playerReader = csv.reader(playersFile)
    for player in playerReader:
        if player[2] != 'G':
            print("Parsing player: " + player[1])
            response = requests.get('https://statsapi.web.nhl.com/api/v1/people/' + player[0] + '/stats?stats=gameLog&season=20212022')
            res = response.json()

            playerInfo = [player[0], player[1], player[2], player[3]]

            sunday = datetime.datetime(2021, 10, 17)
            
            weekInfo = baseWeekInfo.copy()
            seasonInfo = baseWeekInfo.copy()
            weekDifficulty = 0
            lastWeek = None
            resultPPG = 0

            gameList = list(res['stats'][0]['splits'])
            gameList.reverse()
            
            # For game in week X
            for game in gameList:
                if (datetime.datetime.strptime(game['date'], '%Y-%m-%d')) < endDate:
                    if (datetime.datetime.strptime(game['date'], '%Y-%m-%d')) <= sunday:
                        weekInfo = addGame(weekInfo, game)
                        seasonInfo = addGame(seasonInfo, game)
                        resultPPG += game['stat']['powerPlayGoals']
                    else:
                        if (lastWeek != None):
                            # Calculate Difficulty for Week X + 1
                            teamID = game['team']['id']
                            responseUpcoming = requests.get('https://statsapi.web.nhl.com/api/v1/schedule?teamId=' + str(teamID) + '&startDate=' + startDate.strftime("%Y-%m-%d") + '&endDate=' + sunday.strftime("%Y-%m-%d"))
                            upcomingRes = responseUpcoming.json()

                            for upcomingGame in upcomingRes['dates']:
                                weekDifficulty += calculateDifficulty(upcomingGame['games'][0]['teams'], teamID)

                            # print('Write to Week: ' + str(sunday))
                            df.loc[len(df)] = lastWeek + [weekDifficulty] + [resultPPG]

                        row = playerInfo + list(seasonInfo.values()) + list(weekInfo.values())
                        lastWeek = row
                        
                        newDay = datetime.datetime.strptime(game['date'], '%Y-%m-%d')
                        sunday = datetime.datetime.strptime(game['date'], '%Y-%m-%d') + datetime.timedelta(days=6 - newDay.weekday())
                        startDate = sunday - datetime.timedelta(days=6)
                        resultPPG = 0
                        weekInfo = baseWeekInfo.copy()
                        weekInfo = addGame(weekInfo, game)
                        seasonInfo = addGame(seasonInfo, game)
                        resultPPG += game['stat']['powerPlayGoals']
                        weekDifficulty = 0

                        
            # Write last week
            if (lastWeek != None):
                # Calculate Difficulty for Week X + 1
                teamID = game['team']['id']
                responseUpcoming = requests.get('https://statsapi.web.nhl.com/api/v1/schedule?teamId=' + str(teamID) + '&startDate=' + startDate.strftime("%Y-%m-%d") + '&endDate=' + sunday.strftime("%Y-%m-%d"))
                upcomingRes = responseUpcoming.json()

                row = playerInfo + list(seasonInfo.values()) + list(weekInfo.values())

                for upcomingGame in upcomingRes['dates']:
                    weekDifficulty += calculateDifficulty(upcomingGame['games'][0]['teams'], teamID)

                current_df.loc[len(current_df)] = row + [weekDifficulty]

                

print(df.head(10))
df.to_csv('data/data.csv', index=False)
current_df.to_csv('data/current_data.csv')
print("Data saved to data.csv!")
