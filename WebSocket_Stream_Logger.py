from flask import Flask,jsonify
from flask import request,has_request_context
import datetime
import websocket
import json
import time
import os
import asyncio
import hashlib
import logging
from logging.handlers import TimedRotatingFileHandler

#THis is the basic configuration of the logging models


logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s - %(msecs)d - %(levelname)s - %(message)s",
                    datefmt='%Y-%m-%d_%H-%M-%S',
                    filename='C:/BOX_1/binancewebsocketcreation/Main_log/App_Main.log')

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
fileHandler= TimedRotatingFileHandler(filename='C:/BOX_1/binancewebsocketcreation/Main_log/Main_log.log',when="midnight", interval=1 ,backupCount=12)
logger.setLevel(logging.DEBUG)
fileHandler.setFormatter(logFormatter)
logger.addHandler(fileHandler)

#add file handler to access  the logs of the error of the stream
error_handler = TimedRotatingFileHandler('C:/BOX_1/binancewebsocketcreation/error_log/error_log.log',when="midnight",interval=1, backupCount=12)
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(logFormatter)
logger.addHandler(error_handler)

#add file handler to access the logs of the critical errors
critical_handler = TimedRotatingFileHandler('C:/BOX_1/binancewebsocketcreation/critical_error_log/critical_error_log.log',when="midnight",interval=1, backupCount=12)
critical_handler.setLevel(logging.CRITICAL)
critical_handler.setFormatter(logFormatter)
logger.addHandler(critical_handler)

#add file handler to the root logger for the websocket_Stream
Stream_Handler= TimedRotatingFileHandler(filename='C:/BOX_1/binancewebsocketcreation/Web_socket_Stream_logs/websocket_stream_log.log',when="midnight", interval=1 ,backupCount=12)
logger.setLevel(logging.DEBUG)
Stream_Handler.setFormatter(logFormatter)
logger.addHandler(Stream_Handler)
#types of the logs the system is generating.

#logging.info

#logging.error

#logging.warning

#logging.critical

#This is the part of the base app server using flask.

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
    time.sleep(2)
    global LAST_TRADED_PRICE
    LAST_TRADED_PRICE=json.loads(message)
    app.logger.info("program is working as expected.")

    #this adds the data to the logger as well as adds the required data to the stream
    current_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    app.logger.info(f"{current_time} - {message}")
    print(current_time," ",message)

    file_path ='C:/BOX_1/binancewebsocketcreation/Web_socket_Stream_logs/websocket_stream_log.log' #choose your file path
    with open(file_path, "a") as output_file:
            output_file.write(f"{current_time} - {message}\n")

#this takes the part of the error to the logs and from the data stream
def on_error(ws, error):
    app.logger.error("The program encountered an error")
    app.logger.warning("Warning, the program may not function properly")
    
    current_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    app.logger.error(f"{current_time} - {error}")

    # Optionally, you can also log the error to a separate file:

    error_log_file_path ='C:/BOX_1/binancewebsocketcreation/error_log/error_log.log'
    with open(error_log_file_path,"a") as output_file:
        output_file.write(f"{current_time} - {error}\n")


#this takes the part of the critical error from the data stream

def on_close(ws, close_status_code, close_msg):
    app.logger.critical("the connection was lost")
    current_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    app.logger.critical(f"{current_time} - Critical error: {close_msg}")

    # Optionally, you can also log the error to a separate file:

    critical_error_log_file_path = 'C:/BOX_1/binancewebsocketcreation/critical_error_log/critical_error_log.log'
    with open(critical_error_log_file_path,"a") as output_file:
        output_file.write(f"{current_time} - Critical error: {close_msg}\n")

    print("closed the connection")
import time

def reconnect_to_websocket(ws, retry_interval=1):
  """Attempts to reconnect to the WebSocket server.

  Args:
    ws: The WebSocket object.
    retry_interval: The interval between retries in seconds.

  Returns:
    None.
  """

  while True:
    try:
      ws.run_forever()
      return
    except Exception as e:
      logging.error("Failed to reconnect to WebSocket server: %s", e)
      time.sleep(retry_interval)

if __name__ == "__main__":
  ws = websocket.WebSocketApp("ws://localhost:5000")
  reconnect_to_websocket(ws)
"""This function will now attempt to reconnect to the WebSocket server forever, with the specified interval between retries.
If the connection is successful,the function will return. Otherwise, the function will log an error message and sleep for
the specified interval before trying again.Note that it is important to set the retry_interval to a reasonable value. If 
the interval is too short, the function will place a lot of load on the server. If the interval is too long,
the application may not be able to respond to events in a timely manner."""

def handle_websocket_error(ws, error):
   """Handles an error from the WebSocket server.
  
   Args: 
     ws: The WebSocket object. 
     error: The error message. 
   """ 
  
   logging.error("WebSocket error: %s", error)
  
   # Call the `ws.reconnect()` method.
   ws.reconnect()

   # Create a timer to schedule the next reconnect attempt in the future.
   timer = asyncio.create_task(asyncio.sleep(1))
   timer.add_done_callback(lambda timer: handle_websocket_error(ws, error))



def log_data_to_file(file_path, data, append=True):
  """Logs data to a file.

  Args:
    file_path: The path to the file.
    data: The data to log.
    append: Whether to append the data to the file or overwrite it.
  """
  file_path="C:/BOX_1/binancewebsocketcreation/log_data_to_file/log_data_to_file.log"
  try:
    with open(file_path, "a") as output_file:
      output_file.write(data)
      output_file.flush()
  except Exception as e:
    logging.error("Failed to log data to file: %s", e)
  finally:
    if output_file:
      output_file.close()

"""def monitor_program_for_errors(ws, error_threshold=10, error_interval=60):


  error_count = 0
  last_error_time = time.time()

  while True:
    try:
      # TODO: Implement custom monitoring logic here, such as tracking the number of
      # errors that have occurred or monitoring the CPU usage of the program.

      if time.time() - last_error_time > error_interval:
        error_count = 0
        last_error_time = time.time()

      if error_count >= error_threshold:
        return True

      # TODO: Implement custom logic to handle errors, such as logging them or
      # reconnecting to the WebSocket server.

      time.sleep(1)
    except Exception as e:
      logging.error("Failed to monitor program for errors: %s", e)
      return False"""



def back_up_program_configuration_and_data(backup_directory, frequency=3600):
  """Backs up the program's configuration and data.

  Args:
    backup_directory: The directory to store the backups in.
    frequency: The frequency in seconds at which to perform backups.
  """

  while True:
    try:
      backup_directory="C:/BOX_1/binancewebsocketcreation/backup_directory"
      # Get the program's configuration file path.
      configuration_file_path = os.path.join(backup_directory, "config.json")

      # Back up the configuration file to the backup directory.
      with open(configuration_file_path, "rb") as f:
        with open(os.path.join(backup_directory, "config.json.bak"), "wb") as f_out:
          f_out.write(f.read())

      # Verify the integrity of the backup.
      with open(os.path.join(backup_directory, "config.json.bak"), "rb") as f:
        backup_data = f.read()

      backup_hash = hashlib.sha256(backup_data).hexdigest()
      if backup_hash != configuration_file_path.split(".")[0]:
        logging.error("Backup file %s is corrupted", configuration_file_path)
        os.remove(os.path.join(backup_directory, "config.json.bak"))

    except Exception as e:
      logging.error("Failed to back up program configuration and data: %s", e)
      return

    time.sleep(frequency)



url="wss://stream.binance.com:9443/ws/btcusdt@aggTrade"

ws = websocket.WebSocketApp("wss://stream.binance.com:9443/ws/btcusdt@aggTrade",
                            on_open=on_open,
                            on_message=on_message,
                            on_error=handle_websocket_error,
                            on_close=on_close)
# Reconnect to the WebSocket server if the connection is lost.
ws.reconnect_callback = reconnect_to_websocket

# Log all data received from the WebSocket server to a file.
ws.log_data_callback = log_data_to_file

# Monitor the program for errors and performance issues.
#ws.error_monitor_callback = monitor_program_for_errors

# Back up the program's configuration and data every 60 minutes.
ws.backup_callback = back_up_program_configuration_and_data
ws.run_forever()

app.run(host="0.0.0.0",port=5000,debug=True)
