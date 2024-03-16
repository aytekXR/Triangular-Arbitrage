import json
import websocket
import pandas as pd

class BinanceWebSocket:
    def __init__(self, assets):
        self.assets = [coin.lower() + '@bookTicker' for coin in assets]
        self.streams = '/'.join(self.assets)
        self.socket = f"wss://stream.binance.com:9443/stream?streams={self.streams}"

    def on_message(self, ws, message):
        message = json.loads(message)
        print(message)
        print("xxxxxxxxxxxxxxx\n")

    def run(self):
        ws = websocket.WebSocketApp(self.socket, on_message=self.on_message)
        ws.run_forever()

if __name__ == "__main__":
    assets = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT']
    binance_ws = BinanceWebSocket(assets)
    binance_ws.run()
