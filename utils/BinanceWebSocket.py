import json
import websockets
import asyncio

class BinanceWebSocket:
    def __init__(self, assets):
        self.base_url = "wss://stream.binance.com:9443/stream?streams="
        self.assets = [coin.lower() + '@bookTicker' for coin in assets]
        self.ask_prices = {asset: None for asset in self.assets}
        self.streams = '/'.join(self.assets)
        self.socket = f"{self.base_url}{self.streams}"

    async def on_message(self, message):
        message = json.loads(message)
        asset = message['data']['s'].lower() + '@bookTicker'
        ask_price = float(message['data']['a'])  # Convert ask price to float
        if asset in self.ask_prices:
            self.ask_prices[asset] = ask_price

    async def connect(self):
        async with websockets.connect(self.socket) as ws:
            print("Opened connection")
            async for message in ws:
                await self.on_message(message)
            print("Closed connection")

    def get_ask_prices(self):
        return {asset: self.ask_prices[asset] for asset in self.ask_prices if self.ask_prices[asset] is not None}