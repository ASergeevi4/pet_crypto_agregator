from db import create_connection, create_table, insert_data, print_all_coins
from api import fetch_crypto_data, close_cache


DB_NAME = "crypto.db"


def main():
    conn = create_connection(DB_NAME)
    cursor = conn.cursor()

    create_table(cursor)

    data = fetch_crypto_data()
    if data:
        insert_data(cursor, data)
        conn.commit()

    print_all_coins(cursor)

    conn.close()
    close_cache()


if __name__ == "__main__":
    main()