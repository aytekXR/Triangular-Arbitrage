import json
import websockets
import asyncio

class BinanceWebSocket:
    def __init__(self, assets):
        self.base_url = "wss://stream.binance.com:9443/stream?streams="
        self.assets = [coin.lower() + '@bookTicker' for coin in assets]
        self.ask_prices = {asset: 1 for asset in self.assets}
        self.streams = '/'.join(self.assets)
        self.socket = f"{self.base_url}{self.streams}"

    async def on_message(self, ws, message):
        message = json.loads(message)
        # Extract data only if it matches the expected asset format
        if 'data' in message and 's' in message['data'] and 'a' in message['data']:
            asset_symbol = message['data']['s'].lower() + '@bookTicker'
            if asset_symbol in self.ask_prices:
                try:
                    # Ensuring the price is a float and updating the dictionary
                    self.ask_prices[asset_symbol] = float(message['data']['a'])
                except ValueError:
                    # Handles the case where the conversion to float fails
                    print(f"Error converting ask price to float for {asset_symbol}")

    async def on_open(self, ws):
        print("WebSocket connection opened.")

    async def on_close(self, ws, close_status_code, close_msg):
        print("WebSocket connection closed.")

    async def connect(self):
        async with websockets.connect(self.socket) as ws:
            await self.on_open(ws)
            async for message in ws:
                await self.on_message(ws, message)
            await self.on_close(ws, None, None)

    def get_all_ask_prices(self):
        # Filters and returns all ask prices that are not None
        return {asset: price for asset, price in self.ask_prices.items() if price is not None}

    def get_ask_prices(self, sub_assets):
        # Ensure sub_assets are formatted correctly
        formatted_sub_assets = [coin.lower() + '@bookTicker' for coin in sub_assets]
        # Filters and returns ask prices for specified sub_assets
        return {asset: self.ask_prices[asset] for asset in formatted_sub_assets if asset in self.ask_prices}