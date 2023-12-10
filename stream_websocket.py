import websocket
import rel
import logging
import os
from datetime import datetime
import time
from logging.handlers import TimedRotatingFileHandler
import json

def create_logger(currency_pair, currency_type):

    # Create folders for both application and historical data logs with appropriate naming.
    # The `exist_ok=True` argument prevents errors if the folders already exist.
    log_folder = f"historical_data_saver/currency_logs/{currency_type}_currency_logs/{currency_pair}_{currency_type}"
    app_log_folder = f"app_logs/{currency_type}/{currency_pair}_{currency_type}"
    os.makedirs(log_folder, exist_ok=True)
    os.makedirs(app_log_folder, exist_ok=True)

    # Define the logger with the currency pair as its name and set its level to DEBUG.
    logger = logging.getLogger(currency_pair)
    logger.setLevel(logging.DEBUG)

    # Generate the current date for log file naming.
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Create a TimedRotatingFileHandler for application logs.
    # This handler rotates logs at midnight daily, keeping up to 5 backups.
    app_log_file = f"{app_log_folder}/{current_date}_{currency_pair}_{currency_type}.log"
    app_log_file_handler = TimedRotatingFileHandler(filename=app_log_file, when="midnight", interval=1, backupCount=-1)
    app_log_file_handler.setLevel(logging.INFO)  # Set the handler's level to INFO.

    # Create a TimedRotatingFileHandler for historical data logs.
    # This handler rotates logs at midnight daily but keeps all backups (infinite).
    log_file = f"{log_folder}/{current_date}_{currency_pair}_{currency_type}.log"
    file_handler = TimedRotatingFileHandler(filename=log_file, when="midnight", interval=1, backupCount=-1)
    file_handler.setLevel(logging.CRITICAL)  # Set the handler's level to CRITICAL.

    # Define a log formatter to add timestamps, logger names, and messages to the logs.
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
    app_log_file_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add both handlers to the logger.
    logger.addHandler(app_log_file_handler)
    logger.addHandler(file_handler)

    # Finally, return the configured logger object.
    return logger
# Initialize variables

last_update_time = None
currency_pair = None
url = None
currency_type = None
last_message=None
last_message_time=None

def on_message(ws, message):
    try:
        # Parse JSON data
        json_data = json.loads(message)
        symbol = json_data["s"]
        currency_logger.info(f"{message}")
        # Check for repeated messages
        global last_message, last_message_time
        if message == last_message and time.time() - last_message_time <= 5:
            # Same message received within 5 seconds, handle accordingly
            currency_logger.error("Same message received for 5 seconds")
            #behavior for repeated messages
            on_error()
            return

        # Update last message and timestamp
        last_message = message
        last_message_time = time.time()

        # Continue with original message processing logic...

    except Exception as e:
        currency_logger.error(f"Error processing message: {e}")
        on_error()

def on_error(error):
    try:
        currency_logger.error(f"Error connecting to the service: {error}")
        handle_currency(currency_pair, url, currency_type)
    except Exception as e:
        currency_logger.error(f"Error logging error: {e}")
        handle_currency(currency_pair, url, currency_type)

def on_close(close_status_code, close_msg):
    try:
        currency_logger.info(f"Connection closed: Status code {close_status_code}, Message: {close_msg}")
        handle_currency(currency_pair, url, currency_type)
    except Exception as e:
        currency_logger.error(f"Error logging close message: {e}")
        handle_currency(currency_pair, url, currency_type)

def on_open(ws):
    try:
        currency_logger.info("Opened connection")
    except Exception as e:
        currency_logger.error(f"Error logging open message: {e}")


def handle_currency(currency_pair, url, currency_type):
    global currency_logger
    try:
        # Try to create a logger and establish the connection.
        # If anything goes wrong, log the error and stop.
        currency_logger = create_logger(currency_pair, currency_type)
        ws = websocket.WebSocketApp(f"{url}/{currency_pair}@aggTrade",
                                        on_open=on_open,#A callback function that is called when the websocket is opened.
                                        on_message=on_message,#A callback function that is called when the websocket receives a message.
                                        on_error=on_error,#A callback function that is called when the websocket encounters an error.
                                        on_close=on_close)#A callback function that is called when the websocket is closed.
        try:
            # Attempt to run the connection with automatic reconnection.
            # If there are specific connection errors, log them and stop.
            ws.run_forever(dispatcher=rel, reconnect=5)
        except (ConnectionRefusedError, TimeoutError) as e:
            currency_logger.error(f"Connection failed for {currency_pair}: {e}")
        except KeyboardInterrupt:
            # Handle keyboard interrupt gracefully and log information.
            currency_logger.info(f"Connection interrupted for {currency_pair}")

    except (TypeError, ValueError) as e:
        # Catch any issues during logging or message processing.
        currency_logger.error(f"Error handling {currency_pair}: {e}")

    finally:
        # Always attempt to clean up resources. If there are errors, log them.
        try:
            rel.signal(2, rel.abort)
            rel.dispatch()
        except:
            currency_logger.error(f"Error during cleanup for {currency_pair}")
