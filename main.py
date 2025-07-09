import asyncio
import os
import subprocess
import time
from telegram import Bot
from telegram.error import TelegramError
import logging

# Configure logging for better feedback
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Configuration ---
# Replace with your actual bot token from BotFather
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Replace with the Chat ID of the user you want to send the video to.
# This is usually your own user ID for private messages.
TARGET_CHAT_ID = os.getenv("CHANNEL_ID")

# List of video URLs you want to download and send.
# Add more URLs to this list.
VIDEO_URLS = [
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ", # Example YouTube video
    # "https://example.com/another_video.mp4", # Example direct video URL
    # "https://vimeo.com/your_vimeo_video_id", # Example Vimeo video
]

# Directory to temporarily store downloaded videos
DOWNLOAD_DIR = "downloaded_videos"

# Path to the yt-dlp executable.
# If you installed it via pip, 'yt-dlp' should work directly.
# If you downloaded the executable, provide the full path, e.g., r"C:\path\to\yt-dlp.exe" or "/usr/local/bin/yt-dlp"
YT_DLP_PATH = "yt-dlp"

# --- Functions ---

async def download_video(url: str, output_dir: str) -> str | None:
    """
    Downloads a video from the given URL using yt-dlp.
    Attempts to download the best quality video and audio.
    Returns the path to the downloaded video file, or None if download fails.
    """
    os.makedirs(output_dir, exist_ok=True)
    # Define the output template for yt-dlp
    # %(title)s.%(ext)s ensures a clean filename based on video title and extension
    output_template = os.path.join(output_dir, "%(title)s.%(ext)s")

    # yt-dlp command to download best quality video and audio
    # -f bestvideo+bestaudio/best: Selects the best video and audio streams, or just the best overall.
    # --merge-output-format mp4: Merges video and audio into an MP4 container if separate streams are downloaded.
    # --output: Specifies the output filename template.
    command = [
        YT_DLP_PATH,
        "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "--merge-output-format", "mp4",
        "--output", output_template,
        url
    ]

    logging.info(f"Starting download for: {url}")
    try:
        process = subprocess.run(command, capture_output=True, text=True, check=True)
        logging.info(f"Download output for {url}:\n{process.stdout}")

        # yt-dlp prints the final filename to stdout on success.
        # We need to parse it from the output. This is a common pattern.
        # Look for the line that indicates the file has been downloaded.
        downloaded_file = None
        for line in process.stdout.splitlines():
            if "[Merger] Merged" in line or "[download] Destination:" in line:
                # Extract the path from the line, assuming it's quoted or at the end
                # This parsing can be tricky and might need adjustment based on yt-dlp output changes
                if "[Merger] Merged" in line:
                    parts = line.split(" into ")
                    if len(parts) > 1:
                        downloaded_file = parts[1].strip().strip("'\"")
                elif "[download] Destination:" in line:
                    downloaded_file = line.split("Destination:")[1].strip().strip("'\"")
                
                # Check if the extracted path actually exists and is a file
                if downloaded_file and os.path.exists(downloaded_file) and os.path.isfile(downloaded_file):
                    logging.info(f"Successfully downloaded: {downloaded_file}")
                    return downloaded_file
        
        logging.error(f"Could not determine downloaded file path from yt-dlp output for {url}.")
        return None

    except subprocess.CalledProcessError as e:
        logging.error(f"Error downloading {url}: {e.stderr}")
        return None
    except FileNotFoundError:
        logging.error(f"Error: '{YT_DLP_PATH}' not found. Please ensure yt-dlp is installed and in your PATH, or specify the full path.")
        return None
    except Exception as e:
        logging.error(f"An unexpected error occurred during download for {url}: {e}")
        return None

async def send_video_to_telegram(bot: Bot, chat_id: str, video_path: str, caption: str):
    """
    Sends a video file to the specified Telegram chat ID.
    Includes privacy settings and streaming support.
    """
    try:
        logging.info(f"Sending video '{video_path}' to chat ID '{chat_id}'...")
        with open(video_path, 'rb') as video_file:
            await bot.send_video(
                chat_id=chat_id,
                video=video_file,
                caption=caption,
                supports_streaming=True,  # Recommended for better playback
                protect_content=True      # Prevents forwarding and saving
            )
        logging.info(f"Video '{os.path.basename(video_path)}' sent successfully!")
    except TelegramError as e:
        logging.error(f"Failed to send video '{os.path.basename(video_path)}' to Telegram: {e}")
        if "File is too large" in str(e):
            logging.error("This video might exceed Telegram's 2GB file size limit for bots.")
    except FileNotFoundError:
        logging.error(f"Error: Video file not found at '{video_path}' during sending.")
    except Exception as e:
        logging.error(f"An unexpected error occurred while sending video '{os.path.basename(video_path)}': {e}")

async def main():
    """Main function to orchestrate video downloading and sending."""
    if BOT_TOKEN == "YOUR_BOT_TOKEN" or TARGET_CHAT_ID == "YOUR_USER_ID":
        logging.error("Please update BOT_TOKEN and TARGET_CHAT_ID in the script before running.")
        return

    if not VIDEO_URLS:
        logging.warning("No video URLs provided in VIDEO_URLS list. Exiting.")
        return

    bot = Bot(token=BOT_TOKEN)

    # Ensure the download directory exists
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    async with bot:
        for i, url in enumerate(VIDEO_URLS):
            logging.info(f"\n--- Processing video {i + 1}/{len(VIDEO_URLS)}: {url} ---")
            downloaded_path = await download_video(url, DOWNLOAD_DIR)

            if downloaded_path:
                caption = f"Video {i + 1}: {os.path.basename(downloaded_path).split('.')[0]}"
                await send_video_to_telegram(bot, TARGET_CHAT_ID, downloaded_path, caption)
                
                # Clean up the downloaded file after sending
                try:
                    os.remove(downloaded_path)
                    logging.info(f"Cleaned up downloaded file: {downloaded_path}")
                except OSError as e:
                    logging.error(f"Error removing file {downloaded_path}: {e}")
            else:
                logging.error(f"Skipping sending for {url} due to download failure.")

            # Add a small delay to avoid hitting Telegram API rate limits
            if i < len(VIDEO_URLS) - 1:
                logging.info("Waiting 5 seconds before processing next video...")
                await asyncio.sleep(5)

    logging.info("\nAll video processing complete.")

if __name__ == "__main__":
    asyncio.run(main())
 
