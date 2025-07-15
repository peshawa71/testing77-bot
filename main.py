import os
from dotenv import load_dotenv
from telethon.sync import TelegramClient
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument
from telethon.tl.types import InputPeerChannel
import asyncio
import tqdm
# Load .env
load_dotenv()
# api_id = int(os.getenv("API_ID"))
# api_hash = os.getenv("API_HASH")
api_id = int(os.getenv("APITELEGRAM_ID")) 
api_hash = os.getenv("APITELEGRAM_HASH")
channel_to_send = os.getenv("CHANNEL_ID")

DOWNLOADS_DIR = "downloads100"
os.makedirs(DOWNLOADS_DIR, exist_ok=True)

client = TelegramClient("name1", api_id, api_hash)
client.start()

def download_and_forward(chat, limit):
    # isdownload = True
    messages = client.get_messages(chat, limit=limit)

    reverse_data = messages[::-1]

    # all_listed_id = [message.id for message in messages if "چیرۆکی شەوێک" in message.text and message.media]

    # max_id = max(all_listed_id) if all_listed_id else print("No messages found with the specified text and media.")


    for msg in tqdm.tqdm(reverse_data):


        if msg.media and "چیرۆکی شەوێک" in msg.text:


            # for message2 in tqdm.tqdm(messages) if message2.media and "چیرۆکی شەوێک" in message2.text and message2.id == max_id:
            #     current_max_id = msg.id
            #     DOWNLOAD_VIDEO = message2

            

            try:
                
                print(f"\n📥 Downloading media from message ID {msg.id} {msg.text}...")
                filename = client.download_media(msg, DOWNLOADS_DIR)

                if filename:

                    print(f"\n✅ Downloaded: {filename}")

                    # Send to another channel
                    client.send_file(channel_to_send, filename, caption=f"{DOWNLOAD_VIDEO.text}")
                    print(f"🚀 Sent to {channel_to_send}\n")

                    # Delete file
                    os.remove(filename)
                    print(f"🗑️ Deleted {filename}")

            except Exception as e:
                print(f"❌ file Error : {e}")

if __name__ == "__main__":
    source = "@reng_tv"
    limit = 200
    download_and_forward(source, limit)
