import requests

class CoinGeckoFetcher:
    BASE_URL = "https://api.coingecko.com/api/v3/simple/price"



    def fetch_prices(self, coin_ids: list[str], vs_currency: str) -> dict:
        ids_str = ",".join(coin_ids)
        response = requests.get(
            self.BASE_URL,
            params={
                "ids": ids_str,
                "vs_currencies": vs_currency
            }
        )
        if response.status_code == 429:
            raise Exception(f"Rate limit exceeded: {response.status_code} {response.text}")
        if response.status_code != 200:
            raise Exception(f"Failed to fetch prices for {ids_str} in {vs_currency}: {response.status_code} {response.text}")
        data = response.json()
        return {coin_id: data.get(coin_id, {}).get(vs_currency, 0.0) for coin_id in coin_ids}



