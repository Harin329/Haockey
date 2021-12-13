from yahoo_oauth import OAuth2
import json
from dotenv import dotenv_values

config = dotenv_values(".env")

print(config)

creds = {'consumer_key': config['CONSUMER_KEY'], 'consumer_secret': config['CONSUMER_SECRET']}
with open("./auth.json", "w") as f:
   f.write(json.dumps(creds))
oauth = OAuth2(None, None, from_file='./auth.json')