from pydantic import BaseModel
from typing import List


class CoinConfig(BaseModel):
    id: str          # CoinGecko ID, e.g. "bitcoin"
    name: str        # Coin name, e.g. "Bitcoin"
    threshold: float # Price threshold, e.g. 10000
    notify_step: float = 0.05 # Notify step, e.g. 0.05

def get_coin_config() -> List[CoinConfig]:
    return [ 
        CoinConfig(id="bitcoin", name="Bitcoin", threshold=107600, notify_step=0.05),
        CoinConfig(id="ethereum", name="Ethereum", threshold=1000, notify_step=0.05),
        CoinConfig(id="solana", name="Solana", threshold=100, notify_step=0.05),
        CoinConfig(id="dogecoin", name="Dogecoin", threshold=0.1, notify_step=0.05),

    ]
