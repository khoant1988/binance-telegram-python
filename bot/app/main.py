import schedule
import time
from fetch_price import fetch_and_send_price
import logging

# Cấu hình logging
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Schedule the job
schedule.every().day.at("00:05").do(fetch_and_send_price)
schedule.every().day.at("02:50").do(fetch_and_send_price)
schedule.every().day.at("04:05").do(fetch_and_send_price)
schedule.every().day.at("08:05").do(fetch_and_send_price)
schedule.every().day.at("12:05").do(fetch_and_send_price)
schedule.every().day.at("14:30").do(fetch_and_send_price)
schedule.every().day.at("16:20").do(fetch_and_send_price)
schedule.every().day.at("20:05").do(fetch_and_send_price)

# Run the scheduler
if __name__ == "__main__":
    print("Starting Binance to Telegram bot...")
    logging.info("Starting Binance to Telegram bot...")
    while True:
        schedule.run_pending()
        time.sleep(1)