from multiprocessing import Process
from stream_websocket import handle_currency

def run_currency(currency, url):
    try:
        handle_currency(currency, url[0], url[1])
    except Exception as e:
        print(f"Error handling {currency}: {e}")

if __name__ == '__main__':

    ############ ################### This should be from the config ########################
    currencies = ['btcusdt', 'ethusdt', 'xrpusdt']  # List of currencies
    urls = [("wss://fstream.binance.com:/ws", "perpetual"), ("wss://stream.binance.com:9443/ws", "spot")]
    ####################################################################################

    # Create a separate process for each currency
    processes = []
    for url in urls:
        for currency in currencies:
            p = Process(target=run_currency, args=(currency, url))
            processes.append(p)
            p.start()

    # Wait for all processes to complete:
    for process in processes:
        process.join()
