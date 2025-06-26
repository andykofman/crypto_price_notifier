# CoinGeckoAdapter implements PriceFetcher

import requests

class CoinGeckoAdapter:
    BASE_URL = "https://api.coingecko.com/api/v3/simple/price"

    def get_current_price(self, coin_id: str, vs_currency: str) -> float:
        response = requests.get(
            self.BASE_URL,
            params={
                "ids": coin_id,
                "vs_currencies": vs_currency
            }
        )
        if response.status_code != 200:
            raise Exception(f"Failed to fetch price for {coin_id} in {vs_currency}: {response.status_code} {response.text}")

        data = response.json()
        return data.get(coin_id, {}).get(vs_currency, 0.0)


cg = CoinGeckoAdapter()

# Get current price of Bitcoin in USD
price_data = cg.get_current_price('bitcoin', 'usd')
print("Current Bitcoin Price (USD):", price_data)