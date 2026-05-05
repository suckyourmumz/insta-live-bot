import time
import requests

# -------- SETTINGS --------
USERNAME = "elphabaoriona"
WEBHOOK = "https://discordapp.com/api/webhooks/1499156805962698863/vBzHTfB-whjWiZGCx3RRX-0-yim4UUjifTbQZEDlZxzoTQKoy-YPbbavhjc-1boYTOSm"
CHECK_INTERVAL = 2  # faster checks
REQUEST_TIMEOUT = 5
RETRY_COUNT = 3
COOLDOWN = 300  # seconds before allowing another ping
# --------------------------

was_live = False
last_ping_time = 0


def check_live(username):
    url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={username}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "X-IG-App-ID": "936619743392459",
        "Accept": "*/*",
        "Connection": "keep-alive",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache"
    }

    for attempt in range(RETRY_COUNT):
        try:
            r = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)

            print(f"[DEBUG] Status: {r.status_code}")

            if r.status_code != 200:
                print("[WARN] Bad response:", r.text[:200])
                continue

            data = r.json()
            user = data.get("data", {}).get("user", {})

            is_live = user.get("is_live", False)

            print(f"[DEBUG] Live status: {is_live}")

            return is_live

        except Exception as e:
            print(f"[ERROR] Attempt {attempt+1} failed:", e)
            time.sleep(1)

    return False


def send_ping():
    global last_ping_time

    now = time.time()

    # prevent spam if IG flickers live state
    if now - last_ping_time < COOLDOWN:
        print("[INFO] Ping skipped (cooldown)")
        return

    message = {
        "content": f"@everyone 🔴 **{USERNAME} is LIVE on Instagram!**\nhttps://instagram.com/{USERNAME}",
        "allowed_mentions": {"parse": ["everyone"]}
    }

    try:
        r = requests.post(WEBHOOK, json=message, timeout=5)
        print("[INFO] Ping sent:", r.status_code)
        last_ping_time = now
    except Exception as e:
        print("[ERROR] Failed to send webhook:", e)


print("Instagram Live Tracker started...")

while True:
    try:
        live = check_live(USERNAME)

        if live and not was_live:
            print("🔴 LIVE DETECTED")
            send_ping()

        was_live = live

    except Exception as e:
        print("[FATAL ERROR]:", e)

    time.sleep(CHECK_INTERVAL)
