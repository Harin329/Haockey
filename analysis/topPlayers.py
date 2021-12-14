import logging
from logging import config
from yahoo_oauth import OAuth2
import yahoo_fantasy_api as yfa
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
playerID = []

for num in range(10):
    url = "https://fantasysports.yahooapis.com/fantasy/v2/league/411.l.96677/players;start=" + str(num * 25) + ";sort=PTS;count=25/percent_owned"
    print(url)
    response = sc.session.get(url, params={'format': 'json'})
    res = response.json()

    players = list(res['fantasy_content']['league'][1]['players'].values())
    for player in players[:-1]:
        playerID.append({ "id": player['player'][0][1]['player_id'], "name": player['player'][0][2]['name']['full'] })

with open("players.txt", "w") as txt_file:
    for line in playerID:
        txt_file.write(str(line) + "\n")

# playerMapping = {}

# taken = league.taken_players()
# taken = list(map(lambda x: x['player_id'], taken))
# # print(taken)

# faC = league.free_agents('C')
# faC = list(map(lambda x: x['player_id'], faC))

# faW = league.free_agents('W')
# faW = list(map(lambda x: x['player_id'], faW))

# faD = league.free_agents('D')
# faD = list(map(lambda x: x['player_id'], faD))
# # print(faD)

# waivers = league.waivers()
# waivers = list(map(lambda x: x['player_id'], waivers))
# # print(waivers)

# playerDB = taken + faC + faW + faD + waivers

# start = datetime.datetime(2021, 10, 12)
# end = datetime.datetime.now()

# while start <= end:
#     stats = league.player_stats(playerDB, 'date', date=start)
#     for player in stats:
#         name = str(player['player_id']) + "_" + player['name']
#         # stats = list(map(lambda x: [x['name'], x['player_id'], calculateFantasyPoints(x)], stats))
#         if name not in playerMapping:
#             playerMapping[name] = [calculateFantasyPoints(player)]
#         else:
#             p = playerMapping[name]
#             p.append(p[-1] + calculateFantasyPoints(player))
#     start += timedelta(days=1)
#     print(start)


# config.dictConfig({
#     'version': 1,
#     'disable_existing_loggers': True,
# })

# for key, value in playerMapping.items():
#     plt.plot(value, label=key)

# plt.ylabel('Points')
# plt.xlabel('Days')
# plt.legend()
# plt.show()