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

# definitions = {
#     'ID': 'ID',
#     'Name': 'Name',
#     'Position': 'Position',
#     'GP': 'Games Played',
#     'G': 'Goals',
#     'A': 'Assists',
#     'PTS': 'Points',
#     '+/-': 'Plus/Minus',
#     'PIM': 'Penalty Minutes',
#     'PPG': 'Power Play Goals',
#     'PPA': 'Power Play Assists',
#     'PPP': 'Power Play Points',
#     'SHG': 'Short Handed Goals',
#     'GWG': 'Game Winning Goals',
#     'SOG': 'Shots On Goal',
#     'S%': 'Shooting Percentage',
#     'HIT': 'Hits',
#     'BLK': 'Blocks',
#     'PPT': 'Power Play Time',
#     'Avg-PPT': 'Average Power Play Time',
#     'SHT': 'Short Handed Time',
#     'Avg-SHT': 'Average Short Handed Time',
#     'COR': 'Corsi',
#     'FEN': 'Fenwick',
#     'Off-ZS': 'Offensive Zone Starts',
#     'Def-ZS': 'Defense Zone Starts',
#     'ZS-Pct': 'Zone Start Percentage',
#     'GStr': 'Game Star',
#     'Shifts': 'Shifts',
#     'FP': 'Fan Points',
#     'GP_W': 'Games Played This Week',
#     'G_W': 'Goals This Week',
#     'A_W': 'Assists This Week',
#     'PTS_W': 'Points This Week',
#     '+/-_W': 'Plus/Minus This Week',
#     'PIM_W': 'Penalty Minutes This Week',
#     'PPG_W': 'Power Play Goals This Week',
#     'PPA_W': 'Power Play Assists This Week',
#     'PPP_W': 'Power Play Points This Week',
#     'SHG_W': 'Short Handed Goals This Week',
#     'GWG_W': 'Game Winning Goals This Week',
#     'SOG_W': 'Shots On Goal This Week',
#     'S%_W': 'Shooting Percentage This Week',
#     'HIT_W': 'Hits This Week',
#     'BLK_W': 'Blocks This Week',
#     'PPT_W': 'Power Play Time This Week',
#     'Avg-PPT_W': 'Average Power Play Time This Week',
#     'SHT_W': 'Short Handed Time This Week',
#     'Avg-SHT_W': 'Average Short Handed Time This Week',
#     'COR_W': 'Corsi This Week',
#     'FEN_W': 'Fenwick This Week',
#     'Off-ZS_W': 'Offensive Zone Starts This Week',
#     'Def-ZS_W': 'Defense Zone Starts This Week',
#     'ZS-Pct_W': 'Zone Start Percentage This Week',
#     'GStr_W': 'Game Star This Week',
#     'Shifts_W': 'Shifts This Week',
#     'FP_W': 'Fan Points This Week',
#     # 'Team': 'Team',
# }


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