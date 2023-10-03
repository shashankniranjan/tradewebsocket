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

#run the flask application
app.run(host="0.0.0.0",port=50100,debug=True)
