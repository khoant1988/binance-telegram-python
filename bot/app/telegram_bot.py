from telegram import Bot
from dotenv import load_dotenv
import os
import asyncio
import logging

# Cấu hình logging
logging.basicConfig(
    filename='telegram.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Load environment variables
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Initialize Telegram bot
telegram_bot = Bot(token=TELEGRAM_BOT_TOKEN)

# Khởi tạo vòng lặp sự kiện toàn cục
global_loop = asyncio.new_event_loop()
asyncio.set_event_loop(global_loop)

# Hàm bất đồng bộ để gửi tin nhắn
async def send_message(message):
    try:
        await telegram_bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
    except Exception as e:
        logging.error(f"Error sending message: {e}")
        print(f"Error sending message: {e}")

# Hàm gửi tin nhắn đồng bộ
def send_message_sync(message):
    global_loop.run_until_complete(send_message(message))