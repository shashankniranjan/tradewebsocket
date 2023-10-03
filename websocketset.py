import websocket
import json

def on_open(ws):
    print("Opened connection to the stream ")
    try:
        subscribe={ "method": "SUBSCRIBE", "params": ["btcusdt@aggTrade"] , "id": 1}
        ws.send(json.dumps(subscribe))
    except Exception as e:
        print(e)

def on_message(ws, message):
    data=json.loads(message)
    print(data)
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("closed the connection")

url="wss://stream.binance.com:9443/ws/btcusdt@aggTrade"

ws = websocket.WebSocketApp(url,on_open=on_open,on_message=on_message,
                            on_error=on_error,on_close=on_close)
ws.run_forever()