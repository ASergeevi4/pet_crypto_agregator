from db import create_connection, create_table, insert_data, print_all_coins, clear_table, get_price_history
from api import fetch_crypto_data
from cache import clear_cache, close_cache

DB_NAME = "crypto.db"

def main():
    conn = create_connection(DB_NAME)
    cursor = conn.cursor()

    create_table(cursor)

    while True:
        answer = input(""">>> 
Please choose one of the options:
1) Show all coins
2) Make new request
3) Clear table
4) Show price chart
5) Show price history for a coin
6) Exit
>>> """)
        if answer.isdigit() and int(answer) in range(1, 7):
            if answer == "1":
                print_all_coins(cursor)
            elif answer == "2":
                data = fetch_crypto_data()
                if data:
                    insert_data(cursor, data)
                    conn.commit()
            elif answer == "3":
                clear_table(cursor)
                clear_cache()
                print("The table has been cleared")
            elif answer == "4":
                data = fetch_crypto_data()
                if data:
                    from visuals import plot_prices
                    plot_prices(data)
                else:
                    print("No data to display")
            elif answer == "5":
                coin_id = input("Enter the coin ID (e.g. bitcoin): ").lower()
                history = get_price_history(cursor, coin_id)
                from visuals import plot_price_history
                plot_price_history(coin_id, history)
            elif answer == "6":
                print("Exit the program")
                break
        else:
            print("Please enter a number from 1 to 6")

    conn.close()
    close_cache()

if __name__ == "__main__":
    main()
