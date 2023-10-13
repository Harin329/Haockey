from yahoo_oauth import OAuth2
import yahoo_fantasy_api as yfa
import schedule
import time
import boto3
from dotenv import dotenv_values

config = dotenv_values("../auth/.env")

sc = OAuth2(None, None, from_file='../auth/auth.json')
session = boto3.Session(
    aws_access_key_id=config["AWS_ACCESS_KEY"],
    aws_secret_access_key=config["AWS_SECRET_KEY"],
    region_name="us-east-1"
)

if not sc.token_is_valid():
    print("Refreshing Token...")
    sc.refresh_access_token()

# Get League ID
gm = yfa.Game(sc, 'nhl')
print("League ID: " + str(gm.league_ids(year=2023)))

league = yfa.League(sc, '427.l.43850')
print("League Standing: " + str(league.standings()))

team = yfa.Team(sc, '427.l.43850.t.1')
print("Team Roster: " + str(team.roster()))

dynamodb = session.resource('dynamodb')
table = dynamodb.Table('Fantasy')

## Weekly Pickup (Add, Drop)
def pickup():
    print("Weekly Pickup...")
    # List all partition keys in table
    response = table.scan()
    # get partition key for each player
    for player in response['Items']:
        dropID = player['DropID']
        addID = player['AddID']
        try:
            team.add_and_drop_players(addID, dropID)
            print("Dropped " + str(dropID) + " and added " + str(addID))
        except:
            print("Failed to drop " + str(dropID) + " and add " + str(addID))


## Manual Weekly Pickup (Add, Drop)
def manualPickup():
    print("Manual Weekly Pickup...")
    # team.add_and_drop_players(6571, 5366)
    # team.add_and_drop_players(3349, 5391)
    # team.add_and_drop_players(6002, 8287)
    # team.add_and_drop_players()

schedule.every().day.at("00:00").do(pickup)
print("Job Scheduled! Good Luck!")

while True:
    schedule.run_pending()
    time.sleep(1)