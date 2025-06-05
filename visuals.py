import matplotlib.pyplot as plt
import os

def plot_prices(data):
    names = [coin['name'] for coin in data]
    prices = [coin['current_price'] for coin in data]

    plt.style.use('seaborn-v0_8-dark-palette')
    plt.figure(figsize=(12, 6))
    plt.bar(names, prices, color='skyblue')
    plt.title('Top 10 Crypto Prices (USD)')
    plt.xlabel('Cryptocurrency')
    plt.ylabel('Price (USD)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_price_history(coin_id, history, save_path=None):
    if not history:
        print('No price history available')
        return None
    else:
        times = [item[0] for item in history]
        prices = [item[1] for item in history]
        plt.figure(figsize=(10, 5))
        plt.plot(times, prices, marker='o', linestyle='-', color='orange')
        plt.title(f'Price History for {coin_id.capitalize()}')
        plt.xlabel('Timestamp')
        plt.ylabel('Price (USD)')
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        if save_path:
            full_path = os.path.abspath(save_path)
            plt.savefig(full_path)
            print(f'Price history saved to {full_path}')
        else:
            plt.show()
