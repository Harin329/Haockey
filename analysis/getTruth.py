import requests
import csv
import datetime
import pandas as pd

print("==================================Get Truth====================================")
df = pd.DataFrame(columns=["Name", "PPG_W"])
today = datetime.datetime.today()

endDate = today - datetime.timedelta(days=today.weekday()) - datetime.timedelta(hours=today.hour) - datetime.timedelta(minutes=today.minute) - datetime.timedelta(seconds=today.second) - datetime.timedelta(microseconds=today.microsecond)
startDate = endDate - datetime.timedelta(days=7)

with open('data/players.csv', mode ='r') as playersFile:
    playerReader = csv.reader(playersFile)
    for player in playerReader:
        if player[2] != 'G':
            print("Parsing player: " + player[1])
            response = requests.get('https://statsapi.web.nhl.com/api/v1/people/' + player[0] + '/stats?stats=gameLog&season=20212022')
            res = response.json()
            resultPPG = 0

            gameList = list(res['stats'][0]['splits'])
            gameList.reverse()
            
            # For game in week X
            for game in gameList:
                if (datetime.datetime.strptime(game['date'], '%Y-%m-%d')) < endDate and (datetime.datetime.strptime(game['date'], '%Y-%m-%d')) >= startDate:
                        resultPPG += game['stat']['powerPlayGoals']

            df.loc[len(df)] = [player[1]] + [resultPPG]

     
sorted = df.sort_values(['PPG_W'], ascending=[False]).loc[:, ["Name", "PPG_W"]]
print(sorted.head(30)) 
sorted['PPG_W'] = df['PPG_W'].astype(int)

with open("data/truth.csv", "a") as f:
    writer = csv.writer(f)
    writer.writerow(['==================================NEW_WEEK===================================='])
    for player in sorted.nlargest(10, ['PPG_W'], keep='all').itertuples():
        writer.writerow([player[1]])

print("Data saved to truth.csv!")
