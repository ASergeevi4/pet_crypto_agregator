import requests
import sqlite3
import redis
import json

r = redis.Redis(host='localhost', port=6379, db=0)
DB_NAME = 'crypto.db'
COINGECKO_URL = "https://api.coingecko.com/api/v3/coins/markets"
PARAMS = {
    "vs_currency": "usd",
    "order": "market_cap_desc",
    "per_page": 10,
    "page": 1,
    "sparkline": "false"
}


def create_connection(db_name):
    return sqlite3.connect(db_name)


def create_table(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS coins (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        symbol TEXT NOT NULL,
        current_price REAL,
        market_cap REAL,
        last_updated TEXT
    )
    """)


def fetch_crypto_data():
    cache_key = 'crypto_data'
    cached_data = r.get(cache_key)

    if cached_data:
        print('Cached data')
        return json.loads(cached_data)
    
    print('Requesting info from CoinGecko')
    response = requests.get(COINGECKO_URL, params=PARAMS, timeout=6)
    data = response.json()

    r.setex(cache_key, 60, json.dumps(data))

    return data


def insert_data(cursor, data):
    for coin in data:
        cursor.execute("""
        INSERT OR REPLACE INTO coins (id, name, symbol, current_price, market_cap, last_updated)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            coin['id'],
            coin['name'],
            coin['symbol'],
            coin['current_price'],
            coin['market_cap'],
            coin['last_updated']
        ))


def print_all_coins(cursor):
    cursor.execute("SELECT * FROM coins")
    rows = cursor.fetchall()
    for row in rows:
        print(row)


def main():
    conn = create_connection(DB_NAME)
    cursor = conn.cursor()

    create_table(cursor)

    data = fetch_crypto_data()
    insert_data(cursor, data)
    conn.commit()

    print_all_coins(cursor)

    conn.close()


if __name__ == "__main__":
    main()