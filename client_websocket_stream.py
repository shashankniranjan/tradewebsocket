from flask import Flask, request
import requests
from WebSocket_Stream_Logger import LAST_TRADED_PRICE

app = Flask(__name__)

@app.route('/',methods=['GET'])
def get_last_price():
    try:
        response = requests.get('http://localhost:5000/')
        global LAST_TRADED_PRICE
        LAST_TRADED_PRICE = response.json()
    except Exception as e:
        print(f"Error fetching last price: {e}")
        return None

    if LAST_TRADED_PRICE is not None:
        print(f"The last traded price is {LAST_TRADED_PRICE}.")
    else:
        print("No data available.")
        input("Press Enter to fetch again")
        
    return "Last price fetched successfully."

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
