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

    async def on_message(self, ws, message):
        message = json.loads(message)
        asset = message['data']['s'].lower() + '@bookTicker'
        ask_price = float(message['data']['a'])  # Convert ask price to float
        print(message)
        if asset in self.ask_prices:
            self.ask_prices[asset] = ask_price

    async def on_open(self, ws):
        print("Opened connection")

    async def on_close(self, ws, close_status_code, close_msg):
        print("Closed connection")

    async def connect(self):
        async with websockets.connect(self.socket) as ws:
            await self.on_open(ws)
            async for message in ws:
                await self.on_message(ws, message)
            await self.on_close(ws, None, None)
    
    def get_all_ask_prices(self):
        a = {asset: self.ask_prices[asset] for asset in self.ask_prices if self.ask_prices[asset] is not None}
        return a
    
    def get_ask_prices(self, sub_assets):
        # Ensure sub_assets are formatted correctly
        formatted_sub_assets = [coin.lower() + '@bookTicker' for coin in sub_assets]
        # Return a dictionary with the ask prices for the specified sub_assets
        return {asset: self.ask_prices[asset] for asset in formatted_sub_assets if asset in self.ask_prices}
