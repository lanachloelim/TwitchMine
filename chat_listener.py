# chat_listener.py
import os
import argparse
import time
import requests
from datetime import datetime
from twitchio.ext import commands
from dotenv import load_dotenv
import re
import hashlib
import multiprocessing
from pymongo import MongoClient
import certifi


#################################################
# Load environment variables from .env file
#################################################
load_dotenv()
TWITCH_CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")
TWITCH_APP_TOKEN = os.getenv("TWITCH_APP_TOKEN")
TWITCH_OAUTH = os.getenv("TWITCH_OAUTH")
MONGO_URI = os.getenv("MONGO_URI")

def get_stream_info(channel_name, client_id, access_token):
    # Construct API request URL and headers
    url = f"https://api.twitch.tv/helix/streams?user_login={channel_name}"
    headers = {
        "Client-ID": client_id,
        "Authorization": f"Bearer {access_token}"
    }
    # Send GET request and parse JSON response
    response = requests.get(url, headers=headers)
    data = response.json()
    streams = data.get("data")
    if streams:
        # Return the stream info from Twitch API (necessary for indexing MongoDB)
        return streams[0] 
    return None

def run_listener_for_channel(channel, token, client_id, access_token, mongo_uri):
    print(f"Monitoring channel: {channel}")
    while True:
        # Check if the channel is live
        stream_info = get_stream_info(channel, client_id, access_token)
        if stream_info:
            session_start = stream_info["started_at"]  # True stream start time
            print(f"{channel} is live! Starting listener (session_start={session_start})...")
            # Create a new bot instance for this channel
            bot = ChatListenerBot(token, channel, mongo_uri, session_start)
            try:
                # Run the bot (connect to chat and start listening)
                bot.run()
            except Exception as e:
                print(f"Bot error: {e}")
            print(f"{channel} went offline or bot stopped. Waiting for live...")
        else:
            print(f"{channel} is offline. Checking again in 60 seconds...")
            time.sleep(60)


#################################################
# ChatListenerBot class                         
#################################################
class ChatListenerBot(commands.Bot):
    def __init__(self, token, channel, mongo_uri, session_start):
        super().__init__(token=token, prefix='!', initial_channels=[channel])
        self.channel = channel
        self.session_start = session_start
        #self.mongo_client = MongoClient(mongo_uri)
        self.mongo_client = MongoClient(
            MONGO_URI,
            tls=True,
            tlsCAFile=certifi.where()
        )
        self.db = self.mongo_client["twitch_mine"]
        self.collection = self.db[channel]

    async def event_message(self, message):
        user_hash = hashlib.sha256(message.author.name.encode()).hexdigest()[:16]
        sanitized_content = re.sub(
            r'https?://\S+|@\w+',
            lambda m: '<URL>' if m.group(0).startswith('http') else '@<USER>', # Replace URLs and @mentions with placeholders
            message.content
        )   
        ts = datetime.utcnow().isoformat()
        chat_doc = {
            "session_start": self.session_start,  # Twitch stream session start (ISO8601)
            "timestamp": ts,                      # Message timestamp
            "username": user_hash,                # Hashed username
            "content": sanitized_content          # Sanitized chat content
        }
        self.collection.insert_one(chat_doc)


################################################
# MAIN
################################################
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("channels", nargs="+")
    args = parser.parse_args()

    # Twitch API asyncio event loop only exists in a process' main thread
    # Solution: Multiprocessing instead of multithreading - multiple bots listening to different channels
    processes = []
    for channel in args.channels:
        p = multiprocessing.Process(
            target=run_listener_for_channel,
            args=(channel, TWITCH_OAUTH, TWITCH_CLIENT_ID, TWITCH_APP_TOKEN, MONGO_URI),
            daemon=True
        )
        p.start()
        processes.append(p)

    for p in processes:
        p.join()
    
if __name__ == "__main__":
    main()