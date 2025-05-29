import redis
import json

r = redis.Redis(host="localhost", port=6379, db=0)

def get_cache(key):
    cached_data = r.get(key)
    if cached_data:
        print("[Redis] Cached data found")
        return json.loads(cached_data)
    return None

def set_cache(key, data, ttl=60):
    r.setex(key, ttl, json.dumps(data))

def clear_cache(key="crypto_data"):
    r.delete(key)
    print(f"[Redis] Cache for key {key} cleared")

def close_cache():
    r.close()