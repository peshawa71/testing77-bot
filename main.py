from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os


LOCAL_VIDEO_PATH = "video.mp4"
TELEGRAMAPI_ID = os.getenv("APITELEGRAM_ID")   
TELEGRAMAPI_HASH = os.getenv("APITELEGRAM_HASH")
TELEGRAM_TOKEN = os.getenv("BOT_TOKEN")
BOT_USERNAME = "@drama23bot"  # Replace with your bot's username

async def send_video_as_document(video_path: str, caption: str = None):
    """
    Sends a video file to a Telegram channel as a document to preserve quality.

    Args:
        video_path (str): The path to your video file.
        caption (str, optional): An optional caption for the video. Defaults to None.
    """
    bot = Bot(token=TELEGRAM_TOKEN)
    try:
        async with bot:
            with open(video_path, 'rb') as video_file:
                await bot.send_document(
                    chat_id=CHANNEL_ID,
                    document=video_file,
                    caption=caption,
                    parse_mode=ParseMode.HTML # Or ParseMode.MARKDOWN_V2 if you prefer
                )
        print(f"Video '{video_path}' sent successfully as a document to {CHANNEL_ID}")
    except Exception as e:
        print(f"Error sending video: {e}")


# download_media(10, "dramay chall")

video_file_to_send = "video.mp4"  # Path to your video file
video_caption = "Here is the video in full quality."
asyncio.run(send_video_as_document(video_file_to_send, video_caption))
