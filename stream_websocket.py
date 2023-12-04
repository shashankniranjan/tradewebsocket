import websocket
import rel
import logging
import os
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

def create_logger(currency_pair, currency_type):
    """
    This function creates separate loggers for each currency pair and type.

    Args:
        currency_pair: The identifier for the currency pair (e.g., EURUSD).
        currency_type: The type of currency (e.g., forex, crypto).

    Returns:
        A logging object specific to the provided currency pair and type.
    """

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
    app_log_file_handler = TimedRotatingFileHandler(filename=app_log_file, when="midnight", interval=1, backupCount=None)
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