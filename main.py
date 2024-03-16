import asyncio
from utils.BinanceWebSocket import *
from utils.ArbitrageCalculator import *

async def check_arbitrage_opportunity(binance_ws, arbitrage_calculator):
    while True:
        ask_prices = binance_ws.get_ask_prices()
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
