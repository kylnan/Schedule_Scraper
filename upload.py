import requests
import json
import os
from datetime import datetime

JSON_PATH = os.path.join(os.getcwd(), "carvana_schedule.json")
CLOUD_URL = "https://YOUR_CLOUD_URL/convert"

def upload_and_get_ics():
    with open(JSON_PATH, "r") as f:
        data = json.load(f)

    print("📤 Uploading schedule JSON to cloud service...")
    res = requests.post(CLOUD_URL, json=data)

    if res.status_code == 200:
        with open("carvana_schedule.ics", "w") as f:
            f.write(res.text)
        print("✅ ICS file saved as carvana_schedule.ics")
    else:
        print("❌ Failed to convert JSON:", res.status_code, res.text)

upload_and_get_ics()
