from yahoo_oauth import OAuth2
import yahoo_fantasy_api as yfa
import csv
sc = OAuth2(None, None, from_file='../auth/auth.json')

if not sc.token_is_valid():
    print("Refreshing Token...")
    sc.refresh_access_token()

# Get League ID
gm = yfa.Game(sc, 'nhl')
# print("League ID: " + str(gm.league_ids(year=2021)))

league = yfa.League(sc, '411.l.96677')
# print("League Standing: " + str(league.standings()))

team = yfa.Team(sc, '411.l.96677.t.2')
# print("Team Roster: " + str(team.roster()))

playerList = []

for player in team.roster():
    playerList.append(player['name'])

index = 1

with open('predictions.csv', mode ='r') as predictionFile:
    predictionReader = csv.reader(predictionFile)
    for prediction in predictionReader:
        if (prediction[0] in playerList):
            print("#" + str(index) + ": " + prediction[0] + " - " + prediction[1])
        index += 1
