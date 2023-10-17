import time

import requests

import logging
from logging.handlers import TimedRotatingFileHandler

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
file_handler = TimedRotatingFileHandler('BTCUSDT/BTCUSDT-', when="midnight", interval=1, backupCount=7)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)



# No matter what the client should not stop
# it should keep on checking the ltp from flash app
#TODO : Modify code to handle multiple currencies in different thread
def get_last_msg():
    try:
        response = requests.get('http://localhost:4001/ltm')
        logger.info(response.json())
        return response.json()

    except Exception as e:
        logger.error(f"Exception Occured {e}")


if __name__ == "__main__":
    while True:
        ltp = get_last_msg()
        if ltp is not None:
            # this is the main source of historical data
            logger.info(ltp)
        else:
            logger.error("No data available")
