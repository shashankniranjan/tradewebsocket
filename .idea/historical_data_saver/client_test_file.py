import requests
import logging
from logging.handlers import TimedRotatingFileHandler
import requests
from Application import response

# Configure logging
logging.basicConfig(level=logging.DEBUG,
                    format=f"%(asctime)s - %(msecs)d - %(levelname)s - %(message)s",
                    datefmt='%Y-%m-%d_%H-%M-%S',
                    filename='C:/BOX_1/binancewebsocketcreation/clean_websocket_code/Client_logs/client_log.log')

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

class FlaskClient:
    def __init__(self, server_url):
        self.server_url = server_url

    def get_last_price(self):
        response = requests.get(self.server_url + '/ltp')
        if response.status_code == 200:
            return response.json()['last_price']
        else:
            raise Exception('Failed to get last price: {}'.format(response.status_code))
        

    def get_last_msg(self):
        response = requests.get(self.server_url + '/ltm')
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception('Failed to get last msg: {}'.format(response.status_code))

# Example usage:

client = FlaskClient('http://localhost:5000')

def main():
    while True:
        try:
            last_price = client.get_last_price()
            last_msg = client.get_last_msg()

            print('Last price:', last_price)
            print('Last msg:', last_msg)
        except Exception as e:
            print('Error:', e)

if __name__ == '__main__':
    main()
