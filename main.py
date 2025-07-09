import os
from dotenv import load_dotenv
from telethon.sync import TelegramClient
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument
from telethon.tl.types import InputPeerChannel
import asyncio

# Load .env
load_dotenv()
# api_id = int(os.getenv("API_ID"))
# api_hash = os.getenv("API_HASH")
api_id = int(os.getenv("APITELEGRAM_ID")) # Replace with your actual API ID
api_hash = os.getenv("APITELEGRAM_HASH")  # Replace with your actual API Hash
channel_to_send = os.getenv("CHANNEL_ID") # e.g. @mychannel

DOWNLOADS_DIR = "downloads100"
os.makedirs(DOWNLOADS_DIR, exist_ok=True)

client = TelegramClient("name1", api_id, api_hash)
client.start()

def show_progress(current, total):
    percent = int(current * 100 / total) if total else 0
    print(f"\r📥 Downloading... {percent}%", end="")

def download_and_forward(chat, limit):
    messages = client.get_messages(chat, limit=limit)
    for msg in messages:
        if msg.media:
            try:
                filename = client.download_media(msg, DOWNLOADS_DIR, progress_callback=show_progress)
                if filename:
                    print(f"\n✅ Downloaded: {filename}")

                    # Send to another channel
                    client.send_file(channel_to_send, filename, caption="✅ Auto forwarded")
                    print(f"🚀 Sent to {channel_to_send}")

                    # Delete file
                    os.remove(filename)
                    print(f"🗑️ Deleted {filename}")
            except Exception as e:
                print(f"❌ Error: {e}")

if __name__ == "__main__":
    source = os.getenv("CHENALL_SOURCE")
    limit = 50
    download_and_forward(source, limit)
