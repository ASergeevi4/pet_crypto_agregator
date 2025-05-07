import sqlite3

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
