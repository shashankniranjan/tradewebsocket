from flask import Flask,jsonify
from flask import request,has_request_context

import logging
from logging.handlers import TimedRotatingFileHandler
logging.basicConfig(filename="binance.log",level=10,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

#create flask application

logger=logging.getLogger("this is the starting root logger")
logger.setLevel(logging.DEBUG)
#injects the logg data if the data is inside the route or not
class NewFormatter(logging.Formatter):
    def format(self, record):
        if has_request_context():
            record.url = request.url
            record.remote = request.remote_addr
        else:
            record.url=None
            record.remote=None
        return super().format(record)

logFormatter=logging.Formatter('%(asctime)s - %(url)s - %(remote) - %(levelname)s - %(message)s')

#add console handler to the root logger
consoleHandler=logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)

#add file handler to the root logger
fileHandler= TimedRotatingFileHandler(filename='binance.log',when="midnight", interval=1 ,backupCount=7)
fileHandler.setFormatter(logFormatter)
logger.addHandler(fileHandler)

logging.info("hello")
logging.error("hello world")
app = Flask(__name__)

@app.route("/")
def hello():
    app.logger.info("from route handler..")
    return "hello world!!!"

import websocket
import json

def on_open(ws):
    print("Opened connection to the stream ")
    try:
        subscribe={ "method": "SUBSCRIBE", "params": ["btcusdt@aggTrade"] , "id": 1}
        ws.send(json.dumps(subscribe))
    except Exception as e:
        print(e)

def on_message(ws, message):
    data=json.loads(message)
    print(data)
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("closed the connection")

url="wss://stream.binance.com:9443/ws/btcusdt@aggTrade"

ws = websocket.WebSocketApp(url,on_open=on_open,on_message=on_message,
                            on_error=on_error,on_close=on_close)
ws.run_forever()
#run the flask application
app.run(host="0.0.0.0",port=50100,debug=True)
import requests
def get_last_price():
    response = requests.get('http://localhost:5000/ltp')
    data = response.json()
    if 'last price' in data:
        return data['last price']
    else:
        return None
    if __name__ == "___main__":
        while True:
            Ltp = get_last_price()
            if ltp is not None:
                print("Last Traded Price. (ltp)")
            else:
                print("No data available")
            input("press eter to fetch again")