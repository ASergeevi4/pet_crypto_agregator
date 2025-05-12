import requests
import redis
import json

COINGECKO_URL = "https://api.coingecko.com/api/v3/coins/markets"
PARAMS = {
    "vs_currency": "usd",
    "order": "market_cap_desc",
    "per_page": 10,
    "page": 1,
    "sparkline": "false"
}

r = redis.Redis(host='localhost', port=6379, db=0)

def fetch_crypto_data(cache_key="crypto_data", cache_ttl=60):
    cached_data = r.get(cache_key)
    ttl_left = r.ttl(cache_key)
    if cached_data:
        print(f"Cached data ({ttl_left} seconds left)")
        return json.loads(cached_data)
    
    print("Requesting info from CoinGecko")
    try:
        response = requests.get(url=COINGECKO_URL, params=PARAMS, timeout=6)
        response.raise_for_status()
        data = response.json()
        r.setex(cache_key, cache_ttl, json.dumps(data))
        return data
    except requests.exceptions.RequestException as e:
        print(f"The error is {e}")
        return []


def close_cache():
    r.close()