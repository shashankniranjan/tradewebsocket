from flask import Flask,jsonify
from flask import request,has_request_context
import datetime
import websocket
import json
import time
import os
import logging
from logging.handlers import TimedRotatingFileHandler
import time
#THis is the basic configuration of the logging models


logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s - %(msecs)d - %(levelname)s - %(message)s",
                    datefmt='%Y-%m-%d_%H-%M-%S',
                    filename='C:/BOX_1/binancewebsocketcreation/Binance_Websocket_test/Main_log/App_Main.log')

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
logFormatter=logging.Formatter('%(asctime)s - %(msecs)d - %(levelname)s - %(message)s')

#add console handler to the root logger
consoleHandler=logging.StreamHandler()
logger.setLevel(logging.INFO)
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)

#add file handler to the root logger for the app_test
fileHandler= TimedRotatingFileHandler(filename='C:/BOX_1/binancewebsocketcreation/Binance_Websocket_test/Main_log/App_Main.log',when="midnight", interval=1 ,backupCount=12)
logger.setLevel(logging.DEBUG)
fileHandler.setFormatter(logFormatter)
logger.addHandler(fileHandler)

app = Flask(__name__)


@app.route('/')
def last_price():
    app.logger.info("from route handler..")
    return "the last price is"

#This is where the base websocket server is embedded into the application.

def on_open(ws):
    print("Opened connection to the stream ")
    app.logger.debug("this is the stream arriving into the log")
    try:
        subscribe={ "method": "SUBSCRIBE", "params": ["btcusdt@aggTrade"] , "id": 1}
        ws.send(json.dumps(subscribe))
        
    except Exception as e:
        print(e)

# Log the message with the time at which it was received
#this is the part which takes the messsage from the application
def on_message(ws, message):
    
    global LAST_TRADED_PRICE
    LAST_TRADED_PRICE=json.loads(message)
    time.sleep(2)

    app.logger.info("program is working as expected.")

    #this adds the data to the logger as well as adds the required data to the stream
    current_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    app.logger.info(f"{current_time} - {message}")
    print(current_time," ",message)

    file_path ='C:/BOX_1/binancewebsocketcreation/Binance_Websocket_test/Web_socket_Stream_logs/websocket_stream_log.log' #choose your file path
    with open(file_path, "a") as output_file:
            output_file.write(f"{current_time} - {message}\n")
    
#this takes the part of the error to the logs and from the data stream
def on_error(ws, error):
    app.logger.error("The program encountered an error")
    current_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    app.logger.error(f"{current_time} - {error}")

def on_close(ws, close_status_code, close_msg):
    app.logger.critical("the connection was lost")
    current_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    app.logger.critical(f"{current_time} - Critical error: {close_msg}")

    print("closed the connection")


url="wss://stream.binance.com:9443/ws/btcusdt@aggTrade"

ws = websocket.WebSocketApp("wss://stream.binance.com:9443/ws/btcusdt@aggTrade",
                            on_open=on_open,
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close)
ws.run_forever()

app.run(host="0.0.0.0",port=5000,debug=True)
