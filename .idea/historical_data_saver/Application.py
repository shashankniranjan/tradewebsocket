from flask import Flask,jsonify,make_response
import datetime
import websocket
import json
import time
import logging
from logging.handlers import TimedRotatingFileHandler
import time
import threading
import sys

# Create a Flask application instance
app = Flask(__name__)

# Configure the logging module
logging.basicConfig(
  level=logging.INFO,  # Set the logging level to INFO
  format="%(asctime)s - %(msecs)d - %(levelname)s - %(message)s",  # Set the logging format
  datefmt="%Y-%m-%d_%H-%M-%S",  # Set the date format for timestamps
  filename="C:/BOX_1/binancewebsocketcreation/clean_websocket_code/Application_logs/App_Main_logs.log",  # Set the filename for the log file
)

# Create a logger object for the current module
logger = logging.getLogger(__name__)

# Set the logging level for the logger object
logger.setLevel(logging.INFO)


# Import the TimedRotatingFileHandler class from the logging module
from logging.handlers import TimedRotatingFileHandler

# Create a TimedRotatingFileHandler object
fileHandler = TimedRotatingFileHandler(
  filename="C:/BOX_1/binancewebsocketcreation/clean_websocket_code/Application_logs/App_Main_logs.log",
  when="midnight",
  interval=1,
  backupCount=30,
)

# Set the logging level for the handler
fileHandler.setLevel(logging.INFO)

# Create a formatter object
logFormatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

# Set the formatter for the handler
fileHandler.setFormatter(logFormatter)

# Add the handler to the logger
logger.addHandler(fileHandler)



# Initialize variables
last_price = None
last_update_time = None
response = None
symbol = None


@app.route('/ltp')#returns last price for the given asset
#Decorates the get_last_price() function with the route() decorator.
# This decorator registers the get_last_price() function as a handler for the /ltp route.
def get_last_price():
  global last_price, last_update_time, response, trade_data, symbol
#Declares the last_price, last_update_time, response, trade_data, and symbol variables as
#  global variables. This means that these variables can be accessed from within the get_last_price() function.
  try:#Creates a try-except block. The try block contains the code that should be executed.
    # The except block contains the code that should be executed if an exception is raised.
    trade_data = json.loads(response)
    #Attempts to parse the response variable as JSON. If the response variable is not valid JSON, an exception will be raised.
  except Exception as e:
    logging.error(response)
    #Logs the response variable to the error log.

  logging.info(trade_data)
  #Logs the trade_data variable to the info log.

  if 'p' in trade_data:
    #Checks if the p key is present in the trade_data dictionary. The p key stores the last price of the symbol.
    last_price = float(trade_data['p'])#assigns the value of the p key in the trade_data dictionary to the last_price variable.
    #The float() function is used to convert the value to a floating-point number
    symbol = trade_data['s']
    #Assigns the value of the s key in the trade_data dictionary to the symbol variable. The s key stores the symbol of the asset.
    last_update_time = time.time()
    #Assigns the current time to the current_time variable. The time.time() function is used to get the current time.
    current_time = time.time()

    if last_price is not None and last_update_time is not None and current_time - last_update_time <= 5:
      # Checks if the last_price variable is not None, the last_update_time variable is not None,
      #  and the difference between the current time and the last update time is less than or equal to 5 seconds.
      response_data = {
        "last_price": last_price,
        "symbol": symbol,
      }
      logger.info(f"last_price -symbol- {last_price} - {symbol}")
      response = make_response(jsonify(response_data), 200)
      # Creates a response object with the response_data dictionary and a status code of 200.
        # 200 means success
      return response
    # Returns the response object.
    else:
      response_data = {"message": "No recent data available"}
      logger.error(f"last_price -symbol- {last_price} - {symbol}")
      logger.error("message - No recent data available")
      response = make_response(jsonify(response_data), 404)
      return response

@app.route('/ltm')
def get_last_msg():
    global response,symbol
    #Declares the response variable as a global variable. This means that the response variable can be accessed from within the get_last_msg() function.
    return response

#This is where the base websocket server is embedded into the application.

def startWebSocket(currency_pair):
          
        try:
          websocket.enableTrace(True)
          #"""Starts the Binance websocket and sets the trace level to True."""
          url=f"wss://stream.binance.com:9443/ws/{currency_pair}@aggTrade"

          ws = websocket.WebSocketApp(url,
                                  on_open=on_open,
                                  on_message=on_message,
                                  on_error=on_error,
                                  on_close=on_close)
          #Creates a WebSocketApp object. The url parameter is the URL of the Binance websocket.
          #  The on_open, on_message, on_error, and on_close parameters are callback
          #  functions that are called when the websocket is opened, receives a message, encounters an error, or is closed
          ws.run_forever()
          #Starts the websocket.
        except Exception as e:
          app.logger.error(f"Error starting websocket for {currency_pair}: {e}")

def get_websocket_url(currency_pair):
    return f"wss://stream.binance.com:9443/ws/{currency_pair}@aggTrade"
#The symbol of the asset being tracked.


def on_open(ws):
    #Prints a message to the console indicating that the websocket has been opened.
    print("Opened connection to the stream ")
    app.logger.debug("this is the stream arriving into the log")
    # Logs a message to the debug log indicating that the websocket has been opened.

#this is the part which takes the messsage from the application
def on_message(ws, message):
    global response
    #Declares the response variable as a global variable.
    #This means that the response variable can be accessed from within the on_message() function.
    response = message
    #Assigns the value of the message parameter to the response variable.
    app.logger.info("program is working as expected.")
    #Logs a message to the info log indicating that the program is working as expected.

    #this adds the data to the logger as well as adds the required data to the stream
    current_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    #ets the current time and formats it as a string
    app.logger.info(f"{current_time} - {message}")
    print(current_time," ",message)
    
#this takes the part of the error to the logs and from the data stream
def on_error(ws, error):
    #Logs a message to the error log indicating that the program encountered an error.
    app.logger.error("The program encountered an error")
    current_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    app.logger.error(f"{current_time} - {error} - {response}")
    # logger.error(response)
    time.sleep(5)  # Wait for 5 seconds before resubscribing
    ws.close()  # Close the existing WebSocket connection1
    startWebSocket(currency_pair)
    #statement starts a new WebSocket connection. This is necessary because the old WebSocket connection cannot be reused.
      # Reconnect and resubscribe


def on_close(ws,close_status_code, close_msg):
    app.logger.critical("the connection was lost")
    current_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    app.logger.critical(f"{current_time} - Critical error: {close_msg}")

    if close_status_code != 1000:
    # The connection was closed due to an error.
      logging.error(f"Connection closed due to error: {close_msg}")
      startWebSocket(currency_pair)
    else:
    # The connection was closed normally.
        logging.info("Connection closed normally.")
        print("closed the connection")

def startServer():
  """Logs a message to the info log indicating that the startServer() function has been called.

  Raises:
    OSError: If the port is already in use.
  """

  logging.info("Inside startServer()")
  try:
    app.run(host="0.0.0.0", port=5000)
  # Try to start the server.
  # If the port is already in use, the `app.run()` method will raise an `OSError` exception.
  except OSError as error:
    ## Catch the `OSError` exception and handle it gracefully.
    logging.error(f"Port 5000 is already in use: {error}")
    # # Log an error message indicating that the port is already in use.
    sys.exit(1)
    #Starts the Flask server on all interfaces and port 5000

def start_websocket_thread(currency_pair):
  """Starts a new thread to run the Binance websocket."""
  try:
      thread = threading.Thread(target=startWebSocket, args=(currency_pair,))
      #Creates a new Thread object.
      #Specifies the startWebSocket() function as the target function for the thread.

      thread.daemon = True
      #Sets the thread to be a daemon thread.
      #A daemon thread is a thread that runs in the background and does not prevent the main thread from terminating.
      # A non-daemon thread is a thread that must be terminated before the main thread can terminate.
      thread.start()
      return thread
  except Exception as e:
      app.logger.error(f"Error starting websocket thread for {currency_pair}: {e}")
    #Starts the thread.

if __name__ == "__main__":
    try:
        # Create a list of currency pairs
        currency_pairs = ['btcusdt']

        # Create a thread for each currency pair
        for currency_pair in currency_pairs:
            start_websocket_thread(currency_pair)
    
    # Keep the main thread alive until all websocket threads have terminated
        while threading.active_count() > 1:
          time.sleep(1)

        # Start the Flask server
        startServer()
    except Exception as e:
        app.logger.error(f"Error starting application: {e}")
