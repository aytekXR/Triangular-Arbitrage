import json
import websockets
import asyncio

class BinanceWebSocket:
    def __init__(self, assets):
        """
        Initializes the BinanceWebSocket object with a list of assets to monitor.

        Args:
        assets (list): A list of cryptocurrency symbols (e.g., ['BTC', 'ETH']) to monitor.
        """
        # The base URL for the Binance WebSocket API.
        self.base_url = "wss://stream.binance.com:9443/stream?streams="
        # Convert each asset symbol to its lowercase bookTicker format (e.g., 'btcusdt@bookTicker').
        self.assets = [coin.lower() + '@bookTicker' for coin in assets]
        # Initialize a dictionary to store the latest ask prices for each asset.
        self.ask_prices = {asset: 1 for asset in self.assets}
        # Combine all assets into a single stream URL.
        self.streams = '/'.join(self.assets)
        # Complete WebSocket URL including the specified asset streams.
        self.socket = f"{self.base_url}{self.streams}"

    async def on_message(self, ws, message):
        """
        Asynchronous handler for incoming WebSocket messages.

        Parses the message to update the ask price for the corresponding asset.

        Args:
        ws: The WebSocket connection object.
        message (str): The incoming message in JSON format.
        """
        # Deserialize the JSON message to a Python dictionary.
        message = json.loads(message)
        # Check if the message contains the expected data structure.
        if 'data' in message and 's' in message['data'] and 'a' in message['data']:
            # Extract the asset symbol and append '@bookTicker' to match the keys in self.ask_prices.
            asset_symbol = message['data']['s'].lower() + '@bookTicker'
            if asset_symbol in self.ask_prices:
                try:
                    # Update the ask price for the asset, converting the price to a float.
                    self.ask_prices[asset_symbol] = float(message['data']['a'])
                except ValueError:
                    # Handle any errors during float conversion.
                    print(f"Error converting ask price to float for {asset_symbol}")

    async def on_open(self, ws):
        """
        Asynchronous handler called when the WebSocket connection is opened.
        """
        print("WebSocket connection opened.")

    async def on_close(self, ws, close_status_code, close_msg):
        """
        Asynchronous handler called when the WebSocket connection is closed.
        """
        print("WebSocket connection closed.")

    async def connect(self):
        """
        Establishes the WebSocket connection and listens for messages.
        """
        async with websockets.connect(self.socket) as ws:
            # Call the on_open handler.
            await self.on_open(ws)
            # Listen for messages and process them using on_message.
            async for message in ws:
                await self.on_message(ws, message)
            # Call the on_close handler upon closing the connection.
            await self.on_close(ws, None, None)

    def get_all_ask_prices(self):
        """
        Retrieves all ask prices that are not None.

        Returns:
        dict: A dictionary containing all non-None ask prices.
        """
        # Return a filtered dictionary where values are not None.
        return {asset: price for asset, price in self.ask_prices.items() if price is not None}

    def get_ask_prices(self, sub_assets):
        """
        Retrieves the ask prices for specified sub-assets.

        Args:
        sub_assets (list): A list of cryptocurrency symbols to retrieve ask prices for.

        Returns:
        dict: A dictionary containing ask prices for the specified sub-assets.
        """
        # Format sub-assets to match the keys in self.ask_prices.
        formatted_sub_assets = [coin.lower() + '@bookTicker' for coin in sub_assets]
        # Return a filtered dictionary containing only the specified sub-assets.
        return {asset: self.ask_prices[asset] for asset in formatted_sub_assets if asset in self.ask_prices}
