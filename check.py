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
    message = f"📢 Update detected:\n```json\n{json.dumps(data, indent=2)}\n```"
    
    requests.post(WEBHOOK, json={"content": message})
    
    with open("last_hash.txt", "w") as f:
        f.write(current_hash)
