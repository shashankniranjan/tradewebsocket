from flask import Flask
import os
import requests
app = Flask(__name__)

@app.route("/1tp")
def get_last_price():
    response = requests.get('http://localhost:5000/')
    data = response.json()

@app.route("/")
def hello():
    file_path = os.path.join(os.getcwd(), 'C:/BOX_1/binancewebsocketcreation/Web_socket_Stream_logs/websocket_stream_log.log')
    #Open the file in read mode
    with open(file_path, 'r') as f:
        file_contents = f.read()
        # Close the file
        f.close()
        print(file_contents)
            # Print the file contents to the console
        return file_contents





if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

    # Get the last price in a loop
    #while True:
     #   last_price = get_last_price()

        #if last_price is not None:
      #      print(f"The last traded price is {last_price}.")

        #else:
       #     print("No data available.")

        #input("Press Enter to fetch again")
            #last_price = get_last_price()
    #if last_price is not None:
    #   return f"The last traded price is {last_price}."
    #else:
    #    return "No data available."
    #       # Get the path to the file
 #   if 'last price' in data:
 #       return data['last price']
##   else:
 #       return None
    