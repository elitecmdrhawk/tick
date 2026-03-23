import requests
import json
import hashlib
import os
from datetime import datetime

URL = "http://tick.infomancer.uk/galtick.json"
WEBHOOK = os.environ["DISCORD_WEBHOOK"]

def get_hash(data):
    return hashlib.md5(json.dumps(data, sort_keys=True).encode()).hexdigest()

try:
    with open("last_hash.txt", "r") as f:
        last_hash = f.read()
except:
    last_hash = ""

try:
    res = requests.get(URL)
    data = res.json()
except Exception as e:
    print("Error fetching JSON:", e)
    exit(1)

current_hash = get_hash(data)

if current_hash != last_hash:
    try:
        ts = data.get("lastGalaxyTick")

        if ts:
            dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
            date_str = dt.strftime("%Y-%m-%d")
            time_str = dt.strftime("%H:%M:%S")

            message = f"🛰️ Last Galaxy Tick was at {time_str} (game time) on {date_str}"
        else:
            message = f"⚠️ Unexpected JSON format:\n```{json.dumps(data, indent=2)}```"

        requests.post(WEBHOOK, json={"content": message})

        with open("last_hash.txt", "w") as f:
            f.write(current_hash)

    except Exception as e:
        print("Error processing data:", e)
        exit(1)
