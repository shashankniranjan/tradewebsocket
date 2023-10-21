import logging
from logging.handlers import TimedRotatingFileHandler
import requests
from flask import Flask
from Application import response
# Configure logging
logging.basicConfig(level=logging.DEBUG,
                    format=f"%(asctime)s - %(msecs)d - %(levelname)s - %(message)s",
                    datefmt='%Y-%m-%d_%H-%M-%S',
                    filename=f'C:/BOX_1/binancewebsocketcreation/clean_websocket_code/Client_logs/client_log.log')

logger=logging.getLogger("this is the starting root logger")
logger.setLevel(logging.DEBUG)

#This displays how the log would be seen by the user
logFormatter=logging.Formatter(f'%(asctime)s - %(msecs)d - %(levelname)s - %(message)s')

#add console handler to the root logger
consoleHandler=logging.StreamHandler()
logger.setLevel(logging.DEBUG)
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)

#add file handler to the root logger for the app_test
fileHandler= TimedRotatingFileHandler(filename=f'C:/BOX_1/binancewebsocketcreation/clean_websocket_code/Client_logs/client_log.log',when="midnight", interval=1 ,backupCount=7)
logger.setLevel(logging.DEBUG)
fileHandler.setFormatter(logFormatter)
logger.addHandler(fileHandler)

# No matter what the client should not stop
# it should keep on checking the ltp from flash app
#TODO : Modify code to handle multiple currencies in different thread

def get_last_price():
    try:
        global response
        response = requests.get('http://localhost:5000/ltp')
        logger.info(response.json())
        return response.json()

    except Exception as e:
        logger.error(f"Exception Occured {e}")


if __name__ == "__main__":
    while True:
        ltp = get_last_price()
        if ltp is not None:
            # this is the main source of historical data
            logger.info(ltp)
        else:
            logger.error("No data available")