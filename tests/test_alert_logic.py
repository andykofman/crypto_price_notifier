from pycoingecko import CoinGeckoAPI
import pytest
from src.notifier.alert_logic import AlertLogic

cg = CoinGeckoAPI()

# Get current price of Bitcoin in USD
price_data = cg.get_price(ids='bitcoin', vs_currencies='usd')
print("Current Bitcoin Price (USD):", price_data['bitcoin']['usd'])

def test_should_notify_decrease_on_5_percent_drop():
    logic = AlertLogic()
    threshold = 100.0
    step = 0.05  # 5%

    # Simulate reaching the threshold
    logic.evaluate_threshold(100.0, threshold)
    assert logic.has_reached_threshold
    assert logic.last_notified_price == 100.0

    # No notification for a small drop (<5%)
    assert not logic.should_notify_decrease(96.0, threshold, step)  # 4% drop

    # Notification for a 5% drop
    assert logic.should_notify_decrease(95.0, threshold, step)  # 5% drop
    assert logic.last_notified_price == 95.0

    # No notification for a small drop after last notification
    assert not logic.should_notify_decrease(91.0, threshold, step)  # ~4.2% drop from 95

    # Notification for another 5% drop from last notified price
    assert logic.should_notify_decrease(90.0, threshold, step)  # ~5.26% drop from 95
    assert logic.last_notified_price == 90.0