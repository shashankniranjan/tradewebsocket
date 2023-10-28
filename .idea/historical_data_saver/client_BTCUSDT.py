import requests
import logging
from logging.handlers import TimedRotatingFileHandler

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
file_handler = TimedRotatingFileHandler('C:/BOX_1/binancewebsocketcreation/clean_websocket_code/Client_logs/client_log.log', when="midnight", interval=1, backupCount=30)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)
#this call the last message from the websocket server
def get_last_msg():
    try:
        response = requests.get('http://localhost:5000/ltm')
        logger.info(response.json())
        return response.json()

    except Exception as e:
        logger.error(f"Exception Occured {e}")

#this code will run indefinitively and until this prints the data it will keep on running
if __name__ == "__main__":
    while True:
        ltm = get_last_msg()
        if ltm is not None:
            # this is the main source of historical data
            logger.info(ltm)
        else:
            logger.error("No data available")