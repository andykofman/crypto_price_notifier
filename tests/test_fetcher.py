import pytest
from src.notifier.fetcher import CoinGeckoAdapter

@pytest.fixture
def fetcher():
    return CoinGeckoAdapter()

def test_get_current_price(fetcher):
    price = fetcher.get_current_price("bitcoin", "usd")
    assert price > 0

