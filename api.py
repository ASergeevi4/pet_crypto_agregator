import requests
from cache import get_cache, set_cache

COINGECKO_URL = "https://api.coingecko.com/api/v3/coins/markets"
PARAMS = {
    "vs_currency": "usd",
    "order": "market_cap_desc",
    "per_page": 10,
    "page": 1,
    "sparkline": "false"
}

def fetch_crypto_data(cache_key="crypto_data", cache_ttl=60):
    cached_data = get_cache(cache_key)
    if cached_data:
        return cached_data

    print("[API] Requesting info from CoinGecko")
    try:
        response = requests.get(url=COINGECKO_URL, params=PARAMS, timeout=6)
        response.raise_for_status()
        data = response.json()
        set_cache(cache_key, data, cache_ttl)
        return data
    except requests.exceptions.RequestException as e:
        print(f"The error is {e}")
        return []
