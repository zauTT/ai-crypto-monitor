"""CoinGecko API client for fetching cryptocurrency prices."""
import requests
from typing import Tuple


def fetch_crypto_prices() -> Tuple[float, float]:
    """Fetch real BTC and ETH prices from CoinGecko API.

    Returns:
        Tuple[float, float]: Bitcoin and Ethereum prices in USD

    Raises:
        Exception: If API request fails
    """
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()
        btc_price = data["bitcoin"]["usd"]
        eth_price = data["ethereum"]["usd"]

        return btc_price, eth_price

    except requests.RequestException as e:
        raise Exception(f"Failed to fetch crypto prices: {e}")
    except KeyError as e:
        raise Exception(f"Unexpected API response format: {e}")
