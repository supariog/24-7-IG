import os
import base64
import json
import time
import requests
import random
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Instagram Stay-Online Bot is Running!"

def stay_online_logic():
    # 1. Setup Session from Environment Variable
    b64_data = os.getenv("IG_SESSION_B64")
    if not b64_data:
        print("CRITICAL ERROR: IG_SESSION_B64 environment variable is missing!")
        return

    try:
        cookies = json.loads(base64.b64decode(b64_data).decode())
    except Exception as e:
        print(f"Error decoding session string: {e}")
        return

    session = requests.Session()
    session.cookies.update(cookies)
    
    # Use your Webshare Proxy here
    # PROXY_URL = "http://username:password@ip:port"
    # session.proxies = {"http": PROXY_URL, "https": PROXY_URL}

    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "X-IG-App-ID": "936619743392459"
    })

    print("Background thread started. Pinging Instagram...")

    while True:
        try:
            # Subtle action: Fetch a public profile to stay active
            # Use 'instagram' or your own username
            r = session.get("https://www.instagram.com/api/v1/users/web_profile_info/?username=instagram")
            
            if r.status_code == 200:
                print(f"[{time.strftime('%H:%M:%S')}] Heartbeat Success: Active")
            elif r.status_code == 401:
                print("Error: Session expired. Update your IG_SESSION_B64.")
            else:
                print(f"Warning: Received status code {r.status_code}")

            # Wait 15-30 minutes
            time.sleep(random.randint(900, 1800))
            
        except Exception as e:
            print(f"Connection error in background thread: {e}")
            time.sleep(300)

def run():
    # Start the Flask server on port 8080 (Render default)
    app.run(host='0.0.0.0', port=8080)

if __name__ == "__main__":
    # Start the Instagram logic in a separate background thread
    t = Thread(target=stay_online_logic)
    t.daemon = True # Thread dies when main process ends
    t.start()
    
    # Start the web server
    run()
