# CLI entry: python -m notifier monitor …

from plyer import notification

def notify(title: str, message: str):
    try:
        notification.notify(
        title=title,
        message=message,
            app_name="Crypto Notifier",
            timeout=5
        )
    except Exception as e:
        print(f"[NOTIFY] {title}: {message}")

import time
import logging
from apscheduler.schedulers.background import BackgroundScheduler

from notifier.config import get_coin_config
from notifier.fetcher import CoinGeckoFetcher
from notifier.alert_logic import AlertLogic
from notifier.runner import notify

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

fetcher = CoinGeckoFetcher()
scheduler = BackgroundScheduler()
alert_state = {}  # Maps coin_id → AlertLogic instance

# Store coins globally for access in the scheduled job
coins = []

def monitor_all_coins():
    global coins
    coin_ids = [coin.id for coin in coins]
    try:
        prices = fetcher.fetch_prices(coin_ids, "usd")
    except Exception as e:
        logger.error(f"Error fetching prices: {e}")
        return
    for coin in coins:
        current_price = prices.get(coin.id, 0.0)
        logic = alert_state.get(coin.id, AlertLogic())
        logger.info(f"Monitoring {coin.name} at {current_price}")
        if logic.evaluate_threshold(current_price, coin.threshold):
            message = f"{coin.name} has reached {coin.threshold} -> now {current_price:.2f}"
            notify(f"{coin.name} Alert", message)
        if logic.should_notify(current_price, coin.threshold, coin.notify_step):
            message = f"{coin.name} has reached {coin.threshold} -> now {current_price:.2f}"
            notify(f"{coin.name} Alert", message)
        alert_state[coin.id] = logic

def main():
    global coins
    coins = get_coin_config()
    scheduler.add_job(monitor_all_coins, 'interval', seconds=60)
    scheduler.start()
    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        scheduler.shutdown()
        logger.info("Notifier stopped")
