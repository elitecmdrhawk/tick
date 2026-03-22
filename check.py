import requests
import json
import hashlib
import os

URL = "http://tick.infomancer.uk/galtick.json"
WEBHOOK = os.environ["DISCORD_WEBHOOK"]

def get_hash(data):
    return hashlib.md5(json.dumps(data, sort_keys=True).encode()).hexdigest()

# load last hash
try:
    with open("last_hash.txt", "r") as f:
        last_hash = f.read()
except:
    last_hash = ""

# fetch JSON
res = requests.get(URL)
data = res.json()

current_hash = get_hash(data)

if current_hash != last_hash:
    from datetime import datetime

# extract timestamp
ts = data["lastGalaxyTick"]

# parse ISO timestamp
dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))

# format parts
date_str = dt.strftime("%Y-%m-%d")
time_str = dt.strftime("%H:%M:%S")

message = f"🛰️ Last Galaxy Tick was at {time_str} (game time) on {date_str}"
    
    requests.post(WEBHOOK, json={"content": message})
    
    with open("last_hash.txt", "w") as f:
        f.write(current_hash)
