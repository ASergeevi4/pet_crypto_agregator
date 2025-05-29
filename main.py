from db import create_connection, create_table, insert_data, print_all_coins, clear_table
from api import fetch_crypto_data
from cache import clear_cache, close_cache

DB_NAME = "crypto.db"

def main():
    conn = create_connection(DB_NAME)
    cursor = conn.cursor()

    create_table(cursor)

    flag = True
    while flag:
        answer = input(""">>>
Please choose one of the options:
1) Show all coins
2) Make new request
3) Clear table
4) Exit
>>> """)
        if answer.isdigit() and int(answer) in range(1,5):
            if answer == "1":
                print_all_coins(cursor)
            elif answer == "2":
                data = fetch_crypto_data()
                if data:
                    insert_data(cursor, data)
                    conn.commit()
                    print("New data has been added")
            elif answer == "3":
                clear_table(cursor)
                clear_cache()
                print("The table and cache have been cleared")
            elif answer == "4":
                print("Exit the program")
                flag = False
        else:
            print("Please enter number from 1 to 4")

    conn.close()
    close_cache()

if __name__ == "__main__":
    main()
