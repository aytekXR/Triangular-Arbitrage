import asyncio
from utils.BinanceWebSocket import *
from utils.ArbitrageCalculator import *
from utils.helpers import *

async def main():
    # all_assets = get_list_of_supported_pairs('List_of_Supported_Assets.txt')
    all_assets =  ['BTCUSDT', 'ETHUSDT', 'ETHBTC', 'USDTTRY', 'BTCTRY', 'BTCEUR']
    binance_ws = BinanceWebSocket(all_assets)
    arbitrage_calculator = ArbitrageCalculator()

    coins = ['BTC', 'ETH', 'USDT']
    # Run both the WebSocket connection and the arbitrage check concurrently
    await asyncio.gather(
        binance_ws.connect(),
        check_arbitrage_opportunity(binance_ws, arbitrage_calculator.calculate_triangular_arbitrage_availability, coins)
    )

if __name__ == "__main__":
    asyncio.run(main())
