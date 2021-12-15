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

print("==================================Get Data====================================")

# Sample Data
# [GP, G, A, +/-, PPG, PPP, SHG, GWG, SOG, HIT, BLK, G_1, A_1, +/-_1, PPG_1, PPP_1, SHG_1, GWG_1, SOG_1, HIT_1, BLK_1...] --> [PPG] @ Week x + 2 


# Get top 500 NHL players

# For each player, extract format in form of sample data above

# Append processed data into txt file