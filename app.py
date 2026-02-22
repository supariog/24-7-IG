import os, json, base64, time, random
from flask import Flask
from threading import Thread
from instagram_private_api import Client, ClientCookieJar

app = Flask('')

@app.route('/')
def home():
    return "Bot Online"

def bot_logic():
    # 1. Decode session from Render Env
    b64_data = os.getenv("IG_SESSION_B64")
    cookies = json.loads(base64.b64decode(b64_data).decode())
    
    # 2. Setup Client
    cookie_jar = ClientCookieJar()
    # If your session JSON has 'sessionid', 'ds_user_id', etc., map them here:
    cookie_jar.set_cookie(requests.cookies.create_cookie(name='sessionid', value=cookies['sessionid']))
    
    api = Client(username=None, password=None, cookie_jar=cookie_jar)
    
    print("Bot started...")

    while True:
        try:
            # 3. Check DMs
            inbox = api.direct_inbox()
            threads = inbox.get('inbox', {}).get('threads', [])
            
            for thread in threads:
                # Check the latest message
                last_msg = thread.get('items', [])[0]
                if last_msg.get('text', '').lower() == '!ping':
                    thread_id = thread.get('thread_id')
                    api.direct_send_message("Pong!", thread_ids=[thread_id])
                    print("Replied to !ping")

            time.sleep(300) # Wait 5 minutes
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(600)

if __name__ == "__main__":
    Thread(target=bot_logic).start()
    app.run(host='0.0.0.0', port=8080)
