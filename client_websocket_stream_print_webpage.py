from flask import Flask
import os
import requests

app = Flask(__name__)

@app.route('/')
def last_price():
    file_path = os.path.join(os.getcwd(), 'C:/BOX_1/binancewebsocketcreation/Web_socket_Stream_logs/websocket_stream_log.log')

    # Open the file in read mode
    with open(file_path, 'r') as f:
        file_contents = f.read()

    # Close the file
    f.close()

    # Split the file contents into a list of lines
    lines = file_contents.splitlines()

    # Get the last line from the list of lines
    last_line = lines[-1]

    # Return the last line from the function
    return last_line

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)