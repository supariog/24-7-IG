import os
import base64
import json
import time
import random
from instagrapi import Client
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "IG Bot: DM '!ping' to the account to test."

def ig_bot_logic():
    cl = Client()
    
    # 1. SET MOBILE FINGERPRINT (Pixel 5)
    cl.set_device({
        "app_version": "319.0.0.36.115",
        "android_version": 30,
        "android_release": "11",
        "dpi": "420dpi",
        "resolution": "1080x2400",
        "manufacturer": "Google",
        "device": "pixel_5",
        "model": "redfin",
        "cpu": "qcom"
    })

    # 2. LOAD SESSION
    b64_data = os.getenv("IG_SESSION_B64")
    if not b64_data:
        print("Error: IG_SESSION_B64 missing from Render Env!")
        return

    session_data = json.loads(base64.b64decode(b64_data).decode())
    cl.set_settings(session_data)
    
    # Optional: cl.set_proxy("http://user:pass@ip:port")

    print("Bot is live. Listening for !ping...")

    while True:
        try:
            # CHECK UNREAD DMS
            threads = cl.direct_threads(amount=5, selected_filter="unread")
            
            for thread in threads:
                for message in thread.messages:
                    # If someone sends !ping
                    if message.text.lower() == "!ping":
                        print(f"Received !ping from {thread.id}. Sending Pong!")
                        cl.direct_answer(thread.id, "🏓 Pong! I am online and running on Render.")
                        # Mark as read so we don't reply twice
                        cl.direct_thread_mark_as_seen(thread.id)

            # HEARTBEAT (So you see it in Render logs)
            print(f"[{time.strftime('%H:%M:%S')}] Monitoring DMs...")
            
            # Wait 2-5 minutes between checks (Don't go too fast or you'll get banned)
            time.sleep(random.randint(120, 300))
            
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(600) # Wait 10 mins if there's a crash

def run_web():
    app.run(host='0.0.0.0', port=8080)

if __name__ == "__main__":
    # Start the IG logic in background
    t = Thread(target=ig_bot_logic)
    t.daemon = True
    t.start()
    
    # Start the Flask web server
    run_web()
