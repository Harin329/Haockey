import logging
from logging import config
from yahoo_oauth import OAuth2
import yahoo_fantasy_api as yfa
import time
import datetime
from datetime import timedelta
import matplotlib.pyplot as plt


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

print("==================================Analysis====================================")

playerMapping = {}


start = datetime.datetime(2021, 10, 12)
end = datetime.datetime.now()

while start <= end:
    stats = league.player_stats(playerID, 'date', date=start)
    # stats = list(map(lambda x: [x['name'], x['player_id'], calculateFantasyPoints(x)], stats))
    for player in stats:
        name = str(player['player_id']) + "_" + player['name']
        if name not in playerMapping:
            playerMapping[name] = [calculateFantasyPoints(player)]
        else:
            p = playerMapping[name]
            p.append(p[-1] + calculateFantasyPoints(player))
    start += timedelta(days=1)
    print(start)
    time.sleep(5)


config.dictConfig({
    'version': 1,
    'disable_existing_loggers': True,
})

for key, value in playerMapping.items():
    plt.plot(value, label=key)

plt.ylabel('Points')
plt.xlabel('Days')
plt.legend()
plt.show()