import time
from multiprocessing import Process
from stream_websocket import handle_currency
import logging
from logging.handlers import TimedRotatingFileHandler


logger = logging.getLogger(__name__)
# Set the logging level for the logger
logging.basicConfig(filename="crypto_data_logger/App_starter_logs/App_logs.log", level=logging.INFO, format="%(levelname)s - %(msecs)d - %(message)s")
# Create a TimedRotatingFileHandler object
file_handler = TimedRotatingFileHandler(filename="crypto_data_logger/App_starter_logs/App_logs.log", when="midnight", interval=1, backupCount=1000000000)
# Set the logging level for the handler
file_handler.setLevel(logging.INFO)
# Set the formatter for the handler
file_handler.setFormatter(logging.Formatter("%(levelname)s - %(msecs)d - %(message)s"))
# Add the handler to the logger
logger.addHandler(file_handler)
def run_currency(currency, url):
    while True:
        try:
            handle_currency(currency, url[0], url[1])
        except Exception as e:
            logger.error(f"Error handling {currency}: {e}")
            # Wait for a specific time before retrying
            time.sleep(1)

if __name__ == '__main__':

    while True:
        try:
            # Open the "currencies.conf" file in read mode
            with open("crypto_data_logger/currencies.conf", "r") as f:
                # Read the contents of the file and split it into lines
                currencies = f.read().splitlines()
            # Open the "urls.conf" file in read mode
            with open("crypto_data_logger/urls.conf", "r") as f:
                # Initialize an empty list to store URL and stream type pairs
                urls = []
                # Iterate over each line in the file
                for line in f.readlines():
                    # Strip any leading or trailing whitespace
                    line = line.strip()
                    # Check if the line contains a valid URL and stream type pair
                    if len(line.split(",")) == 2:
                        # Split the line into URL and stream type
                        url, stream_type = line.split(",")
                        # Add the URL and stream type pair to the list
                        urls.append((url, stream_type))
            # Break out of the loop if no errors occurred
            break
        except Exception as e:
            # Handle any exceptions that occur while reading the configuration files
            logger.error(f"Error reading configuration files: {e}")
            # Wait for a specified time (1 seconds in this case) before retrying
            time.sleep(1)
    while True:
        try:
            # Create a list to store the processes
            processes = []
            # Iterate over each URL
            for url in urls:
                # Iterate over each currency
                for currency in currencies:
                    # Create a new process to handle the currency and URL pair
                    p = Process(target=run_currency, args=(currency, url))
                    # Add the process to the list
                    processes.append(p)
                    # Start the process
                    p.start()
            # Wait for all processes to finish before retrying
            for process in processes:
                process.join()
            # Break out of the loop if no errors occurred
            break
        except Exception as e:
            # Handle any exceptions that occur while creating or starting processes
            logger.error(f"Error creating and starting processes: {e}")
            # Wait for a specified time (1 seconds in this case) before retrying
            time.sleep(1)

