import time
import requests

# -------- SETTINGS --------
USERNAME = "elphabaoriona"
WEBHOOK = "https://discordapp.com/api/webhooks/1499156805962698863/vBzHTfB-whjWiZGCx3RRX-0-yim4UUjifTbQZEDlZxzoTQKoy-YPbbavhjc-1boYTOSm"
CHECK_INTERVAL = 5  # seconds
# --------------------------

was_live = False

def check_live(username):
    url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={username}"

    headers = {
        "User-Agent": "Mozilla/5.0",
        "X-IG-App-ID": "936619743392459"
    }

    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        return False

    data = r.json()
    user = data.get("data", {}).get("user", {})

    return user.get("is_live", False)

def send_ping():
    message = {
        "content": f"@everyone 🔴 **{USERNAME} is LIVE on Instagram!**\nhttps://instagram.com/{USERNAME}",
        "allowed_mentions": {"parse": ["everyone"]}
    }

    requests.post(WEBHOOK, json=message)

print("Instagram Live Tracker started...")

while True:
    try:
        live = check_live(USERNAME)

        if live and not was_live:
            print("LIVE DETECTED")
            send_ping()

        was_live = live

    except Exception as e:
        print("Error:", e)

    time.sleep(CHECK_INTERVAL)