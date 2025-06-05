from db import create_connection, create_table, insert_data, print_all_coins, clear_table, get_price_history
from api import fetch_crypto_data
from cache import clear_cache, close_cache
from visuals import plot_prices, plot_price_history


DB_NAME = "crypto.db"

def main():
    conn = create_connection(DB_NAME)
    cursor = conn.cursor()
    coin_id = None
    history = None
    create_table(cursor)

    while True:
        answer = input(""">>> 
Please choose one of the options:
1) Show all coins
2) Make new request
3) Clear table
4) Show price chart
5) Show price history for a coin
6) Save price history
7) Exit
>>> """)
        if answer.isdigit() and int(answer) in range(1, 8):
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
                    plot_prices(data)
                else:
                    print("No data to display")

            elif answer == "5":
                coin_id = input("Enter the coin ID (e.g. bitcoin): ").lower()
                history = get_price_history(cursor, coin_id)
                plot_price_history(coin_id, history)

            elif answer == "6":
                if history:
                    save_path = input("Enter the path and extension to save the price history: ")
                    plot_price_history(coin_id, history, save_path=save_path)
                else:
                    print("No price history to display. Please choose option 5 first")

            elif answer == "7":
                print("Exit the program")
                break

        else:
            print("Please enter a number from 1 to 7")

    conn.close()
    close_cache()

if __name__ == "__main__":
    main()
