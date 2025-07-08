from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os


LOCAL_VIDEO_PATH = "video.mp4"
TELEGRAMAPI_ID = os.getenv("APITELEGRAM_ID")   
TELEGRAMAPI_HASH = os.getenv("APITELEGRAM_HASH")
TELEGRAM_TOKEN = os.getenv("BOT_TOKEN")
BOT_USERNAME = "@drama23bot"  # Replace with your bot's username


def download_media(number_download):

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
        channelmy = client(GetFullChannelRequest(idpostchennal))
        # print(channelmy.full_chat)

        messages = client.get_messages(channelmy.full_chat, limit=2000)

        i = 1

        for message in tqdm(messages):
            if i == number_download:
                break
            message.download_media('./' + f'/number {i}')
            i += 1


        
 
        return "completed"

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome! Send me a command to download media.")

def handle_response(text: str):
    if "hello" in text.lower():
        return "Hello! How can I assist you today?"
    elif "help" in text.lower():
        return "You can use commands like 'download <number>' to download media."

    # if not text:
    #     return "Please provide a command."
    # if text.startswith("download"):
    #     try:
    #         number_download = int(text.split()[1])
    #         result = download_media(number_download)
    #         return f"Download completed: {result}"
    #     except (IndexError, ValueError):
    #         return "Please provide a valid number after 'download'."
    # else:
    #     return "Unknown command. Use 'download <number>' to download media."



async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type = update.message.chat.type
    message_id = update.message.chat.id
    message_text = update.message.text

    print(f"Received message: .. type :  {message_type} id : {message_id} txt : {message_text}")

    if message_type == "group":
        if BOT_USERNAME in message_text:
            new_user_message = message_text.replace(BOT_USERNAME, "").strip()
            response = handle_response(new_user_message)
        else:
            return "Please mention the bot to get a response."
    else:
        response = handle_response(message_text)
    
    print(f"Response: {response}")
    await update.message.reply_text(response)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f" update : {update} caused err : {context.error}")


if name == "__main__":
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))

    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    app.add_error_handler(handle_message)


    print("Bot is running...")
    app.run_polling(pulling_interval=2)

