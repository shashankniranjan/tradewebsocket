import websocket
import rel
import logging
import os
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

# Function to create a logger for each currency
def create_logger(currency_pair, currency_type):
    log_folder = f"logs/{currency_type}/{currency_pair}_{currency_type}"
    app_log_folder = f"app_logs/{currency_type}/{currency_pair}_{currency_type}"
    os.makedirs(log_folder, exist_ok=True)
    os.makedirs(app_log_folder, exist_ok=True)

    logger = logging.getLogger(currency_pair)
    logger.setLevel(logging.DEBUG)
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Create a app_log_file_handler

    app_log_file = f"{app_log_folder}/{current_date}_{currency_pair}_{currency_type}.log"
    # Import the TimedRotatingFileHandler class from the logging module# Create a TimedRotatingFileHandler object
    app_log_file_handler = TimedRotatingFileHandler(filename=app_log_file, when="midnight", interval=1, backupCount=5)
    app_log_file_handler.setLevel(logging.INFO)


    # Create a file handler

    log_file = f"{log_folder}/{current_date}_{currency_pair}_{currency_type}.log"
    # Import the TimedRotatingFileHandler class from the logging module# Create a TimedRotatingFileHandler object
    file_handler = TimedRotatingFileHandler(filename=log_file, when="midnight", interval=1, backupCount=-1)
    file_handler.setLevel(logging.CRITICAL)

    # Create a log formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
    app_log_file_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(app_log_file_handler)
    logger.addHandler(file_handler)

    return logger


def on_message(ws, message):
    currency_logger.critical(message)  # Log message using currency-specific logger .

def on_error(ws, error):
    currency_logger.error(error)  # Log error using currency-specific logger

def on_close(ws, close_status_code, close_msg):
    currency_logger.info("### closed ###")  # Log close message using currency-specific logger

def on_open(ws):
    currency_logger.info("Opened connection")  # Log connection open using currency-specific logger

def handle_currency(currency_pair , url , currency_type):
    global currency_logger
    currency_logger = create_logger(currency_pair, currency_type)

    ws = websocket.WebSocketApp(f"{url}/{currency_pair}@aggTrade",
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)


    ws.run_forever(dispatcher=rel, reconnect=5)  # Set dispatcher to automatic reconnection, 5 second reconnect delay if connection closed unexpectedly
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch()