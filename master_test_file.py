from flask import Flask,jsonify
from flask import request,has_request_context

import websocket
import json

import logging
from logging.handlers import TimedRotatingFileHandler

#THis is the basic configuration of the logging models


logging.basicConfig(filename=f"app_test.log",level=10,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',filemode='w')

#create flask application

logger=logging.getLogger("this is the starting root logger")
logger.setLevel(logging.INFO)

#injects the log data if the data is inside the route or not

class NewFormatter(logging.Formatter):
    def format(self, record):
        if has_request_context():
            record.url = request.url
            record.remote = request.remote_addr
        else:
            record.url=None
            record.remote=None
        return super().format(record)

#This displays how the log would be seen by the user
logFormatter=logging.Formatter('%(asctime)s - %(message)s')

#add console handler to the root logger
consoleHandler=logging.StreamHandler()
logger.setLevel(logging.INFO)
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)

#add file handler to the root logger for the app_test
fileHandler= TimedRotatingFileHandler(filename='C:/BOX_1/binancewebsocketcreation/main_log/app_test.log',when="midnight", interval=1 ,backupCount=7)
logger.setLevel(logging.DEBUG)
fileHandler.setFormatter(logFormatter)
logger.addHandler(fileHandler)

error_handler = TimedRotatingFileHandler('C:/BOX_1/binancewebsocketcreation/error_logs/app_error_test.log',when="midnight",interval=1, backupCount=7)
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(logFormatter)
logger.addHandler(error_handler)

# attempt 2 of the logging system
#logger1 = logging.getLogger('app_test.area1')
#logger2 = logging.getLogger('app_test.area2')

#types of the logs the system is generating.

#logging.info

#logging.error

#logging.warning

#logging.critical

#This is the part of the base app server using flask.

app = Flask(__name__)

@app.route("/")
def hello():
    app.logger.info("from route handler..")
    return "application start"

#This is where the base websocket server is embedded into the application.

def on_open(ws):
    print("Opened connection to the stream ")
    logger.debug("this is the stream arriving into the log")
    try:
        subscribe={ "method": "SUBSCRIBE", "params": ["btcusdt@aggTrade"] , "id": 1}
        ws.send(json.dumps(subscribe))
    except Exception as e:
        print(e)

def on_message(ws, message):
    data=json.loads(message)
    logger.info("program is working as expected.")
    print(message)

def on_error(ws, error):
    logger.error("The program encountered an error")
    logger.warning("Warning, the program may not function properly")

def on_close(ws, close_status_code, close_msg):
    logger.critical("the connection was lost")
    print("closed the connection")


### url="wss://stream.binance.com:9443/ws/btcusdt@aggTrade"

ws = websocket.WebSocketApp("wss://stream.binance.com:9443/ws/btcusdt@aggTrade",on_open=on_open,
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close)
ws.run_forever()
#import requests
#def get_last_price():
#    response = requests.get('http://localhost:5000/ltp')
#   data = response.json()
#    if 'last price' in data:
##
#    else:
#        return None
##    if __name__ == "__main__":
#        while True:
#            Ltp = get_last_price()
#            if ltp is not None:
#                print("Last Traded Price. (ltp)")
#3\               print("No data available")
#           input("press enter to fetch again")
#run the flask application
app.run(host="0.0.0.0",port=50100,debug=True)