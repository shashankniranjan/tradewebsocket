import threading
import time
import websocket
from flask import Flask, jsonify, make_response
import logging
from logging.handlers import TimedRotatingFileHandler
import json

# Your WebSocket code
# TODO :
# TEST
# Code should not exit on any error
# Code should reconnect in 1 sec after any error
# In case data is not received for 5 secs . We should reconnect to stream
# Run the code for 24HRS+



# Flask code

app = Flask(__name__)

# Define your routes as you've done


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
file_handler = TimedRotatingFileHandler('C:/BOX_1/binancewebsocketcreation/clean_websocket_code/Application_logs/App_Main_logs.log', when="midnight", interval=1, backupCount=7)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)

last_price = None
last_update_time = None
response = None


@app.route('/ltm')
def get_last_msg():
    return response

@app.route('/ltp')
def get_last_price():
    global last_price, last_update_time, response
    try:
        trade_data = json.loads(response)
    except Exception as e:
        logging.error(response)

    logging.info(trade_data)

    if 'p' in trade_data:
        last_price = float(trade_data['p'])
        last_update_time = time.time()
        current_time = time.time()
        if last_price is not None and last_update_time is not None and current_time - last_update_time <= 5:
            response_data = {"last_price": last_price}
            logger.info("last_price - " + str(last_price))
            response = make_response(jsonify(response_data), 200)  # 200 means success
            return response
        else:
            response_data = {"message": "No recent data available"}
            logger.error("last_price - " + str(last_price))
            logger.error("message - No recent data available")
            response = make_response(jsonify(response_data), 404)
            return response


@app.route('/')
def home():
    return "WebSocket Example with Flask"


# make it generic such that it can save any crypo currecy and not just BTCUSDT
# every currency should steam on different thread

def startWebSocket():
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://stream.binance.com/ws/btcusdt@aggTrade",
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.run_forever()  # Remove the dispatcher argument to run the WebSocket in the main thread


# Test this method to see what happens if the program fails
def on_error(ws, error):
    logger.error(response)
    time.sleep(1)  # Wait for 5 seconds before resubscribing
    ws.close()  # Close the existing WebSocket connection
    startWebSocket()  # Reconnect and resubscribe


def on_close(ws, close_status_code, close_msg):
    print("### closed ###")


def on_open(ws):
    print("Opened connection")
    logging.info("Starting Server")


def on_message(ws, message):
    logging.info(f"message -  {message}")
    global response
    response = message


def startServer():
    logging.info("Inside startServer()")
    app.run(host='0.0.0.0', port=5000)


if __name__ == "__main__":
    # Create two threads, one for the WebSocket and one for the Flask server
    websocket_thread = threading.Thread(target=startWebSocket)
    server_thread = threading.Thread(target=startServer)

    # Start both threads
    websocket_thread.start()
    server_thread.start()

    # Wait for both threads to finish (if needed)
    websocket_thread.join()
    server_thread.join()