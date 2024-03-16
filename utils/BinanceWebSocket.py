import json
import websocket

class BinanceWebSocket:
    def __init__(self, assets):
        self.base_url = "wss://stream.binance.com:9443/stream?streams="
        self.assets = [coin.lower() + '@bookTicker' for coin in assets]
        self.ask_prices = {asset: None for asset in self.assets}  # Initialize ask prices dict
        self.update_url()
        self.ws = None

    def update_url(self):
        self.streams = '/'.join(self.assets)
        self.socket = f"{self.base_url}{self.streams}"

    def on_message(self, ws, message):
        message = json.loads(message)
        # Extract the asset and its ask price from the message
        asset = message['data']['s'].lower() + '@bookTicker'
        ask_price = message['data']['a']
        # Update the ask price in the state
        if asset in self.ask_prices:
            self.ask_prices[asset] = ask_price
        print(message)
        print("xxxxxxxxxxxxxxx\n")

    def on_open(self, ws):
        print("Opened connection")

    def on_close(self, ws, close_status_code, close_msg):
        print("Closed connection")

    def add_assets(self, new_assets):
        new_streams = [coin.lower() + '@bookTicker' for coin in new_assets]
        self.assets.extend(new_streams)
        # Update ask_prices dict with new assets
        for asset in new_streams:
            self.ask_prices[asset] = None
        self.update_url()
        if self.ws:
            subscribe_message = json.dumps({
                "method": "SUBSCRIBE",
                "params": new_streams,
                "id": 1
            })
            self.ws.send(subscribe_message)

    def get_ask_prices(self):
        # Return a list of the latest ask prices for subscribed assets
        return [self.ask_prices[asset] for asset in self.ask_prices if self.ask_prices[asset] is not None]
    

    def run(self):
        self.ws = websocket.WebSocketApp(self.socket,
                                         on_message=self.on_message,
                                         on_open=self.on_open,
                                         on_close=self.on_close)
        self.ws.run_forever()
