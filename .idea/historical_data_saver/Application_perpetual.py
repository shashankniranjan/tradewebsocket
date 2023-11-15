from email import message
from flask import Flask,jsonify,make_response
import datetime
import websocket
import json
import time
import logging
from logging.handlers import TimedRotatingFileHandler
import time
import threading
import pytz
import os

# Create a Flask application instance
app = Flask(__name__)
# Create a logger object for the current module
logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(msecs)d - %(message)s')

file_handler = TimedRotatingFileHandler("Application_perpetual_logs/App_Main_perpetual_logs.log", when="midnight", interval=1, backupCount=None)# Import the TimedRotatingFileHandler class from the logging module# Create a TimedRotatingFileHandler object
file_handler.setLevel(logging.INFO) # Set the logging level for the logger object
file_handler.setFormatter(logging.Formatter(f"%(levelname)s - %(msecs)d - %(message)s"))# Set the formatter for the handler
logger.addHandler(file_handler)# Add the handler to the logger

# Initialize variables
last_price = None
last_update_time = None
response = None
symbol = None
currency_pair=None
currency_pairs=None

@app.route('/ltp')#returns last price for the given asset
#Decorates the get_last_price() function with the route() decorator.
# This decorator regutcers the get_last_price() function as a handler for the /ltp route.
def get_last_price():
    global last_price, last_update_time, response, trade_data, symbol
    #Declares the last_price, last_update_time, response, trade_data, and symbol variables as
    #  global variables. This means that these variables can be accessed from within the get_last_price() function.
    try:#Creates a try-except block. The try block contains the code that should be executed.
        # The except block contains the code that should be executed if an exception is raised.
        trade_data = json.loads(response)
        #Attempts to parse the response variable as JSON. If the response variable is not valid JSON, an exception will be raised.
    except Exception as e:
        logger.error(response)
        #Logs the response variable to the error log.

    logger.info(trade_data)
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
    global response
    #Declares the response variable as a global variable. This means that the response variable can be accessed from within the get_last_msg() function.
    return response

def startWebSocket(currency_pair):
    # This line defines the startWebSocket() function with a single parameter, currency_pair
    # . The currency_pair parameter is the name of the currency pair that the websocket should be started for.
    while True:
#This line creates a while True loop.
#  This means that the code will keep trying to start the websocket until it is successful.
        try:
            url = f"wss://fstream.binance.com:/ws/{currency_pair}@aggTrade"
            ws = websocket.WebSocketApp(url,#The URL of the Binance websocket server.
                                        on_open=on_open,#A callback function that is called when the websocket is opened.
                                        on_message=on_message,#A callback function that is called when the websocket receives a message.
                                        on_error=on_error,#A callback function that is called when the websocket encounters an error.
                                        on_close=on_close)#A callback function that is called when the websocket is closed.
            ws.run_forever()
            #This line calls the run_forever() method on the WebSocketApp object to start the websocket.
            break
        #This line breaks out of the while True loop if the websocket is successfully started.
        except Exception as e:
            logging.error(f"Error starting websocket for {currency_pair}: {e}")
            #This line catches any exceptions that occur while starting the websocket and logs an error message.
            time.sleep(1)

def on_open(ws):
    #Prints a message to the console indicating that the websocket has been opened.
    print("Opened connection to the stream ")
    logger.debug("this is the stream arriving into the log")
    # Logs a message to the debug log indicating that the websocket has been opened.

#this is the part which takes the messsage from the application
def on_message(ws, message):
    global response, symbol

    # Declares the response variable as a global variable.
    # This means that the response variable can be accessed from within the on_message() function.
    response = message

    # Assigns the value of the message parameter to the response variable.
    try:
        # Convert the message to a JSON object
        json_data = json.loads(message)

        # Extract the symbol from the JSON object
        symbol = json_data["s"]

        timezone = pytz.timezone('UTC')
        current_time = datetime.datetime.now(timezone).strftime('%Y-%m-%d_%H-%M-%S-%z')
        timezone_offset = datetime.datetime.now(timezone).utcoffset()
        logger.info(f"{current_time} {timezone} {timezone_offset} - {message}")
        print(current_time, " ", message)

        # Create a symbol-specific log file path
        symbol_file_path = f"currency_logs/Perpetual_currency_logs/{symbol}/{symbol}_perpetual_logs.log"

        # Check if the symbol-specific log file exists
        if not os.path.exists(symbol_file_path):
            # Create the symbol-specific log file if it doesn't exist
            with open(symbol_file_path, "w") as f:
                f.write("")

        # Open the symbol-specific log file in append mode
        with open(symbol_file_path, "a") as f:
            # Write the message to the symbol-specific log file
            f.write(f"{current_time} {message}\n")

        # Log the message to the main log file
        logger.info(f"{current_time} {timezone} {timezone_offset} - {message}\n")
    except Exception as e:
        # Handle any errors that occur during processing
        logger.error(f"Error processing message: {e}")


#this takes the part of the error to the logs and from the data stream
def on_error(ws, error):
    #Logs a message to the error log indicating that the program encountered an error.
    logger.error("The program encountered an error")
    timezone = pytz.timezone('UTC')
    current_time = datetime.datetime.now(timezone).strftime('%Y-%m-%d_%H-%M-%S-%z')
    timezone_offset = datetime.datetime.now(timezone).utcoffset()
    logger.error(f"{current_time} {timezone} {timezone_offset} - {error} - {response}")
    # logger.error(response)
    time.sleep(1)  # Wait for 1 seconds before resubscribing
    ws.close() # Close the exutcing WebSocket connection
    startWebSocket(currency_pair)
    #statement starts a new WebSocket connection. This is necessary because the old WebSocket connection cannot be reused.
    # Reconnect and resubscribe

def on_close(ws, close_status_code, close_msg):
    """Logs a critical message indicating that the connection was lost and restarts the websocket connection if the connection was closed due to an error."""
    timezone = pytz.timezone('UTC')
    current_time = datetime.datetime.now(timezone).strftime('%Y-%m-%d_%H-%M-%S-%z')
    timezone_offset = datetime.datetime.now(timezone).utcoffset()
    logger.critical(f"{current_time} {timezone} {timezone_offset} - Critical error: {close_msg}")

    if close_status_code != 1000:
        logger.error(f"Connection closed due to error: {close_msg}")
        startWebSocket(currency_pair)
    else:
        logger.info("Connection closed normally.")

def start_websocket_thread(currency_pair):
    try:
            thread = threading.Thread(target=startWebSocket, args=(currency_pair,))
            #Creates a new Thread object.
            #Specifies the startWebSocket() function as the target function for the thread.

            thread.daemon = True
            #Sets the thread to be a daemon thread.
            #A daemon thread is a thread that runs in the background and does not prevent the main thread from terminating.
            # A non-daemon thread is a thread that must be terminated before the main thread can terminate.
            try:
                thread.start()
            except:
                    logger.error("the thread failed to start")
            return thread
    except Exception as e:
            logger.error(f"Error starting websocket thread for {currency_pair}: {e}")
            #Starts the thread.

def create_directories_for_each_currency(currency_pairs, folder_path):
    global response

    # Declares the response variable as a global variable.
    # This means that the response variable can be accessed from within the on_message() function.
    response = message

    # Creates a directory for each currency in the list of currency pairs.
    for currency_pair in currency_pairs:
        if currency_pair:
            directory_name = currency_pair.split("/")[0]
            full_path = os.path.join(folder_path, directory_name)

            # Create a new logger for each thread
            thread_logger = logging.getLogger(f"thread_{currency_pair}")

            # Use the thread-specific logger to create the directory
            try:
                os.makedirs(full_path, exist_ok=True)
                thread_logger.info(f"Created directory for currency pair: {currency_pair}")
            except Exception as e:
                thread_logger.error(f"Failed to create directory for currency pair: {currency_pair} - {e}")


def startServer():
    """Starts the server on port 5000."""
    logger.info("Inside startServer()")

    # Try to run the app on port 5000.
    try:
        app.run(host="0.0.0.0", port=5000)

    # If an error occurs, log it.
    except Exception as error:
        logger.error(f"{error}")

if __name__ == "__main__":
    try:
        # Start the server thread
        server_thread = threading.Thread(target=startServer)
        server_thread.daemon = True
        server_thread.start()

        # Load the currency pairs from the configuration file
        with open("configuration_files/configuration_perpetual_file.conf", "r") as f:
            currency_pairs = f.read().splitlines()

        # Create an empty lutc to store the websocket threads
        threads = []

        # Iterate over the lutc of currency pairs and start a new websocket thread for each currency pair
        for currency_pair in currency_pairs:
            thread = start_websocket_thread(currency_pair)
        
            # If the websocket thread was successfully created and started, add it to the lutc
            if thread is not None:
                threads.append(thread)

        # Create a directory for each currency in the list of currency pairs.
        folder_path = f"currency_logs/Perpetual_currency_logs"
        create_directories_for_each_currency(currency_pairs, folder_path)

    finally:
        # Wait for all of the websocket threads to finish running
                thread.join()

        # If the program closed unexpectedly, log an error message
                logger.error("the program closed unexpectedly")

