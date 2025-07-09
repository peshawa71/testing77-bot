import requests
import os
import time
from tqdm import tqdm
from telethon.sync import TelegramClient, events
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.types import InputPeerEmpty
from tqdm import tqdm
import os
import asyncio
from telegram import Bot
from telegram.constants import ParseMode # Import ParseMode for potential captions


# Replace with your actual bot token and channel ID
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')  # Or use the numerical ID like -1001234567890
number_download = 5
namefile = "lenawewe"
TELEGRAMAPI_ID = os.getenv('APITELEGRAM_ID')
TELEGRAMAPI_HASH = os.getenv('APITELEGRAM_HASH')
  # Change this to your desired file name prefix
# def send_video_as_document_sync(video_path: str, caption: str = None):
#     """
#     Sends a video file to a Telegram channel as a document using requests (synchronous).

#     Args:
#         video_path (str): The path to your video file.
#         caption (str, optional): An optional caption for the video. Defaults to None.
#     """


with TelegramClient('name1', TELEGRAMAPI_ID, TELEGRAMAPI_HASH) as client:
# Connect to Telegram (if not already connected)
# client.connect() test75.py allcodes for sending* HAZIR <=

    result = client(
        GetDialogsRequest(
            offset_date=None,
            offset_id=0,
            offset_peer="username", # Corrected: InputPeerEmpty needs to be instantiated
            limit=500,                    # Corrected: 'linit' should be 'limit'
            hash=0
        )
    )

    # tittle = "chiyrokiy shewek چیرۆکی شەوێک"
    idpostchennal = 2384585674
    idpostchennal = 1255523166
    channelmy = client(GetFullChannelRequest(idpostchennal))
    # print(channelmy.full_chat)

    messages = client.get_messages(channelmy.full_chat, limit=2000)

    i = 1

    for message in tqdm(messages):
        if i == number_download:
            break
        message.download_media('./' + f'/{namefile} {i}')

        time.sleep(3)  # Optional: Sleep to avoid hitting API rate limits
        video_file_to_send = './' + f'{namefile} {i}'
        video_caption = "Here's the video without quality loss!"
        video_path = video_file_to_send  # Use the downloaded file path

        if not os.path.exists(video_path):
            print(f"Error: Video file not found at '{video_path}'")
            break

        telegram_api_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"

        # Prepare the payload for the request
        data = {
            'chat_id': CHANNEL_ID,
            'caption': caption if caption else '', # Ensure caption is not None for the API call
            'parse_mode': 'HTML' # Or 'MarkdownV2'
        }

        try:
            with open(video_path, 'rb') as video_file:
                files = {'document': video_file}
                response = requests.post(telegram_api_url, data=data, files=files)
                response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

            json_response = response.json()
            if json_response.get('ok'):
                print(f"Video '{video_path}' sent successfully as a document to {CHANNEL_ID}")
            else:
                print(f"Failed to send video. Telegram API response: {json_response.get('description', 'Unknown error')}")

        except requests.exceptions.RequestException as e:
            print(f"Error sending video (network or API error): {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        i += 1

 # <--- IMPORTANT: Change this to your video file path







# if __name__ == '__main__':
#     video_file_to_send = 'path/to/your/video.mp4'  # <--- IMPORTANT: Change this to your video file path
#     video_caption = "Here's the video without quality loss!"

#     # Call the synchronous function
#     send_video_as_document_sync(video_file_to_send, video_caption)
