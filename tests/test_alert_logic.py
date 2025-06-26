from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()

# Get current price of Bitcoin in USD
price_data = cg.get_price(ids='bitcoin', vs_currencies='usd')
print("Current Bitcoin Price (USD):", price_data['bitcoin']['usd'])