from flask import Flask
import os
import requests
app = Flask(__name__)
#@app.route("/")
#def hello():
#    file_path = os.path.join(os.getcwd(), 'C:/BOX_1/binancewebsocketcreation/Web_socket_Stream_logs/websocket_stream_log.log')
#    #Open the file in read mode
#    with open(file_path, 'r') as f:
#        file_contents = f.read()
#        # Close the file
#        f.close()
#        print(file_contents)
#            # Print the file contents to the console
#        return file_contents
from flask import Flask, request
import requests

app = Flask(__name__)

@app.route('/ltp',methods=['GET'])
def get_last_price():
    try:
        response = requests.get('http://localhost:5000/')
        get_last_price = response.json()
    except Exception as e:
        print(f"Error fetching last price: {e}")
        return None

    if get_last_price is not None:
        print(f"The last traded price is {get_last_price}.")
    else:
        print("No data available.")
        input("Press Enter to fetch again")

    return "Last price fetched successfully."

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
    