# CLI entry: python -m notifier monitor …

from plyer import notification
import sys

def play_sound(sound_type: str):
    """
    Play different sounds based on notification type.
    sound_type: 'threshold' for initial threshold crossing, 'movement' for subsequent alerts
    """
    try:
        if sys.platform == "win32":
            import winsound
            if sound_type == "threshold":
                # Higher pitched sound for threshold crossing (more urgent)
                winsound.Beep(1000, 500)  # Higher frequency, longer duration
            else:
                # Lower pitched sound for price movements
                winsound.Beep(800, 300)  # Lower frequency, shorter duration
        else:
            import os
            if sound_type == "threshold":
                # Multiple beeps for threshold crossing on Unix systems
                os.system('printf "\a\a\a"')
            else:
                # Single beep for price movements
                os.system('printf "\a"')
    except Exception as sound_err:
        print(f"[SOUND ERROR] {sound_err}")

def notify(title: str, message: str, alert_type: str = "movement"):
    """
    Send notification with appropriate sound based on alert type.
    alert_type: 'threshold' for initial threshold crossing, 'movement' for subsequent alerts
    """
    try:
        # Use different notification icons/types based on alert type
        if alert_type == "threshold":
            # More urgent notification for threshold crossing
            notification.notify(
                title=f"🚨 {title}",  # Add warning emoji
                message=message,
                app_name="Crypto Notifier",
                timeout=10  # Longer timeout for important alerts
            )
        else:
            # Standard notification for price movements
            notification.notify(
                title=title,
                message=message,
                app_name="Crypto Notifier",
                timeout=5
            )
        
        # Play appropriate sound
        play_sound(alert_type)
        
    except Exception as e:
        print(f"[NOTIFY] {title}: {message}")

import time
import logging
from apscheduler.schedulers.background import BackgroundScheduler

from notifier.config import get_coin_config
from notifier.fetcher import CoinGeckoFetcher
from notifier.alert_logic import AlertLogic

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
        
        # Check for threshold crossing (initial alert)
        if logic.evaluate_threshold(current_price, coin.threshold):
            message = f"{coin.name} has dropped below {coin.threshold} -> now {current_price:.2f}"
            notify(f"{coin.name} Threshold Alert", message, "threshold")
        
        # Check for subsequent price movements
        if logic.should_notify(current_price, coin.threshold, coin.notify_step):
            # Determine if this is an increase or decrease notification
            if logic.last_direction == "decrease":
                message = f"{coin.name} continues dropping -> now {current_price:.2f}"
                notify(f"{coin.name} Price Drop", message, "movement")
            else:
                message = f"{coin.name} recovering -> now {current_price:.2f}"
                notify(f"{coin.name} Price Recovery", message, "movement")
        
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
