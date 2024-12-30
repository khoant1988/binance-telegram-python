from binance.client import Client
from telegram_bot import send_message_sync
from dotenv import load_dotenv
import os
import logging
import time
from datetime import datetime, timedelta

# Cấu hình logging
logging.basicConfig(
    filename='fetch_price.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Load environment variables
load_dotenv()

BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")

# Initialize Binance client
binance_client = Client(api_key=BINANCE_API_KEY, api_secret=BINANCE_API_SECRET)

# Đọc cặp tiền từ file
def get_trading_pairs(file_path="pairs.txt"):
    try:
        abs_path = os.path.join(os.path.dirname(__file__), file_path)
        with open(abs_path, "r") as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        logging.error(f"{file_path} not found.")
        return []

def fetch_and_send_price():
    try:
        pairs = get_trading_pairs()
        for pair in pairs:
            logging.info(f"Pair: {pair}")
            print(f"Pair: {pair}")
            klines = binance_client.get_klines(symbol=pair, interval=Client.KLINE_INTERVAL_4HOUR, limit=3)
            if len(klines) >= 2:
                current_candle = klines[1]  # Cây nến hiện tại
                previous_candle = klines[0]  # Cây nến trước đó

                # Xác định xem có phải bullish pinbar không
                if identify_bullish_pinbar(current_candle, previous_candle):
                    open_price = float(current_candle[1])
                    high_price = float(current_candle[2])
                    low_price = float(current_candle[3])
                    close_price = float(current_candle[4])

                    message = (
                        f"4H Bullish Pinbar Detected for {pair} (GMT+7):\n"
                        f"Open: ${open_price}\n"
                        f"High: ${high_price}\n"
                        f"Low: ${low_price}\n"
                        f"Close: ${close_price}\n"
                    )
                    send_message_sync(message)
                    print(f"Bullish pinbar message for {pair} sent to Telegram.")
                    time.sleep(1)  # Giới hạn tốc độ gửi tin nhắn
    except Exception as e:
        logging.error(f"Error fetching price: {e}")
        print(f"Error fetching price: {e}")

def identify_bullish_pinbar(current_candle, previous_candle):
    """
    Xác định pinbar tăng giá dựa vào cây nến hiện tại và trước đó.

    current_candle: dict chứa thông tin cửa nến hiện tại (open, high, low, close).
    previous_candle: dict chứa thông tin cửa nến trước đó (open, high, low, close).

    Returns: True nếu đáp ứng tiêu chí pinbar tăng giá, ngược lại False.
    """
    try:
        open_price = float(current_candle[1])
        high_price = float(current_candle[2])
        low_price = float(current_candle[3])
        close_price = float(current_candle[4])

        # Tiêu chí 1: High > Close > Open
        if not (close_price > open_price):
            return False

        # Tính toán các thành phần nến
        body = abs(close_price - open_price)
        lower_wick = abs(open_price - low_price)
        upper_wick = abs(high_price - close_price)
        total_range = abs(high_price - low_price)

        # Tiêu chí 2: 0.1 * Lower Wick < Body < 0.3 * Lower Wick
        if not (body > lower_wick/3):
            return False

        # Tiêu chí 3: Body < 0.5 * Upper Wick
        # if (body < upper_wick):
        #     return False

        # Tiêu chí 4: Low < Low của cây nến trước đó
        previous_low = float(previous_candle[3])
        if not (low_price < previous_low):
            return False
        
        # Tiêu chí 5: Open > (high + low) / 2
        if (open_price <= (high_price + low_price) / 2):
            return False

         # Tiêu chí 6 : Đuôi nến dài ít nhất 2/3 chiều dài tổng thể của nến
        if not (lower_wick < total_range * 2/3):
            return False

        return True 
    except Exception as e:
        logging.error(f"Error identifying pinbar: {e}")
        return False