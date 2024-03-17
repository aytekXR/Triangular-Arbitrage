import asyncio
import json
import websockets

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

    def get_all_ask_prices(self):
        return {asset: self.ask_prices[asset] for asset in self.ask_prices if self.ask_prices[asset] is not None}

class ArbitrageCalculator:
    def calculate_triangular_arbitrage_availability(self, rates):
        # Simplified example assuming we're checking for BTC->ETH->USDT->BTC arbitrage loop
        try:
            btc_to_eth = 1 / rates['ethbtc@bookTicker']
            eth_to_usdt = rates['ethusdt@bookTicker']
            usdt_to_btc = 1 / rates['btcusdt@bookTicker']
            
            final_btc = 1 * btc_to_eth * eth_to_usdt * usdt_to_btc
            return final_btc > 1
        except KeyError as e:
            print(f"Missing rate for currency pair: {e}")
            return False
        except ZeroDivisionError:
            print("Encountered division by zero due to a rate being 0.")
            return False

async def check_arbitrage_opportunity(binance_ws, arbitrage_calculator):
    while True:
        ask_prices = binance_ws.get_all_ask_prices()
        if ask_prices:
            opportunity_exists = arbitrage_calculator.calculate_triangular_arbitrage_availability(ask_prices)
            print(f"Arbitrage Opportunity: {'Yes' if opportunity_exists else 'No'}")
        await asyncio.sleep(1)

async def main():
    assets = ['BTCUSDT', 'ETHBTC', 'ETHUSDT']
    binance_ws = BinanceWebSocket(assets)
    arbitrage_calculator = ArbitrageCalculator()
    # Run both the WebSocket connection and the arbitrage check concurrently
    await asyncio.gather(
        binance_ws.connect(),
        check_arbitrage_opportunity(binance_ws,arbitrage_calculator)
    )

if __name__ == "__main__":
    asyncio.run(main())
