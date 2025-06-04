import sqlite3
from datetime import datetime

DB_NAME = "crypto.db"

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

    cursor.execute("""CREATE TABLE IF NOT EXISTS price_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        coin_id TEXT NOT NULL,
        price REAL NOT NULL,
        timestamp TEXT NOT NULL)""")


def insert_data(cursor, data):
    for coin in data:
        last_updated = datetime.fromisoformat(coin['last_updated'].replace('Z', ''))

        cursor.execute("""
        INSERT OR REPLACE INTO coins (id, name, symbol, current_price, market_cap, last_updated)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            coin['id'],
            coin['name'],
            coin['symbol'],
            coin['current_price'],
            coin['market_cap'],
            last_updated.strftime('%Y-%m-%d %H:%M:%S'),
        ))

        cursor.execute("""INSERT INTO price_history (coin_id, price, timestamp)
        VALUES (?, ?, ?)""", (
            coin['id'],
            coin['current_price'],
            last_updated.strftime('%Y-%m-%d %H:%M:%S')
        ))


def get_price_history(cursor, coin_id):
    cursor.execute("""
    SELECT timestamp, price FROM price_history
    WHERE coin_id = ?
    ORDER BY timestamp
    """, (coin_id,))
    return cursor.fetchall()


def print_all_coins(cursor):
    cursor.execute("SELECT * FROM coins")
    rows = cursor.fetchall()
    if rows:
        for row in rows:
            print(row)
        return len(rows)
    return 0


def clear_table(cursor):
    cursor.execute('DELETE FROM coins')