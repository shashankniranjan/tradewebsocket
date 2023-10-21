from flask import Flask,jsonify,make_response
from flask import request,has_request_context
import datetime
import websocket
import json
import time
import logging
from logging.handlers import TimedRotatingFileHandler
import time
import threading

app = Flask(__name__)
#THis is the basic configuration of the logging models
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(msecs)d - %(levelname)s - %(message)s",
                    datefmt='%Y-%m-%d_%H-%M-%S',
                    filename='C:/BOX_1/binancewebsocketcreation/clean_websocket_code/Application_logs/App_Main_logs.log')

logger=logging.getLogger(__name__)
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
logFormatter=logging.Formatter(f'%(asctime)s - %(msecs)d - %(levelname)s - %(message)s')

#add console handler to the root logger
consoleHandler=logging.StreamHandler()
logger.setLevel(logging.INFO)
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)

#add file handler to the root logger for the app_test
fileHandler= TimedRotatingFileHandler(filename='C:/BOX_1/binancewebsocketcreation/clean_websocket_code/Application_logs/App_Main_logs.log',when="midnight", interval=1 ,backupCount=12)
logger.setLevel(logging.INFO)
fileHandler.setFormatter(logFormatter)
logger.addHandler(fileHandler)

websocket_handler= TimedRotatingFileHandler(filename='C:/BOX_1/binancewebsocketcreation/clean_websocket_code/websocket_logs/websocket_logs.log',when="midnight", interval=1 ,backupCount=12)
logger.setLevel(logging.INFO)
websocket_handler.setFormatter(logFormatter)
logger.addHandler(websocket_handler)

last_price = None
last_update_time = None
response = None
symbol=None
@app.route('/ltm')
def get_last_msg():
    return response

@app.route('/ltp')#returns last price for the given asset
def get_last_price():
  global last_price, last_update_time, response, trade_data, symbol

  try:
    trade_data = json.loads(response)
  except Exception as e:
    logging.error(response)

  logging.info(trade_data)

  if 'p' in trade_data:
    last_price = float(trade_data['p'])
    symbol = trade_data['s']
    last_update_time = time.time()
    current_time = time.time()

    if last_price is not None and last_update_time is not None and current_time - last_update_time <= 5:
      response_data = {
        "last_price": last_price,
        "symbol": symbol,
      }
      logger.info(f"last_price -symbol- {last_price} - {symbol}")
      response = make_response(jsonify(response_data), 200)  # 200 means success
      return response
    else:
      response_data = {"message": "No recent data available"}
      logger.error(f"last_price -symbol- {last_price} - {symbol}")
      logger.error("message - No recent data available")
      response = make_response(jsonify(response_data), 404)
      return response

#This is where the base websocket server is embedded into the application.
@app.route('/')
def home():
    return "WebSocket Connected"

def startWebSocket(currency_pair):
    websocket.enableTrace(True)
    url=f"wss://stream.binance.com:9443/ws/{currency_pair}@aggTrade"

    ws = websocket.WebSocketApp(url,
                            on_open=on_open,
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close)
    ws.run_forever()


def get_websocket_url(currency_pair):
    return f"wss://stream.binance.com:9443/ws/{currency_pair}@aggTrade"


def on_open(ws):
    print("Opened connection to the stream ")
    app.logger.debug("this is the stream arriving into the log")

#this is the part which takes the messsage from the application
def on_message(ws, message):
    global response
    response = message
    app.logger.info("program is working as expected.")

    #this adds the data to the logger as well as adds the required data to the stream
    current_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    app.logger.info(f"{current_time} - {message}")
    print(current_time," ",message)

    file_path ='C:/BOX_1/binancewebsocketcreation/clean_websocket_code/websocket_logs/websocket_logs.log' #choose your file path
    with open(file_path, "a") as output_file:
            output_file.write(f"{current_time} - {message}\n")
    
#this takes the part of the error to the logs and from the data stream
def on_error(ws, error):
    app.logger.error("The program encountered an error")
    current_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    app.logger.error(f"{current_time} - {error} - {response}")
    # logger.error(response)
    time.sleep(1)  # Wait for 5 seconds before resubscribing
    ws.close()  # Close the existing WebSocket connection1
    startWebSocket(currency_pair)  # Reconnect and resubscribe


def on_close(ws, close_msg):
    app.logger.critical("the connection was lost")
    current_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    app.logger.critical(f"{current_time} - Critical error: {close_msg}")

    print("closed the connection")

def startServer():
    logging.info("Inside startServer()")
    ++app.run(host="0.0.0.0",port=5000)

def start_websocket_thread(currency_pair):
    thread = threading.Thread(target=startWebSocket, args=(currency_pair,))
    thread.start()

if __name__ == "__main__":
    # Create a list of currency pairs
    currency_pairs = ['btcusdt', 'ethusdt', 'bnbusdt']

    # Create a thread for each currency pair
    for currency_pair in currency_pairs:
        start_websocket_thread(currency_pair)

    # Start the Flask server
    startServer()

