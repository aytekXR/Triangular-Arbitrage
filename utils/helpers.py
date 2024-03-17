import asyncio

async def check_arbitrage_opportunity(binance_ws, calculator, coins):
    """
    Continuously checks for arbitrage opportunities based on the given coins and calculator function.

    Args:
        binance_ws: An instance of BinanceWebSocket to fetch live ask prices.
        calculator: A function that calculates the arbitrage opportunity score.
        coins: A list of coin symbols to check for arbitrage opportunities.
    """
    while True:
        # Generate asset pairs from the list of coins and fetch their current ask prices
        ask_prices = binance_ws.get_ask_prices(create_asset_pairs(coins))
        
        if ask_prices:
            # Calculate the arbitrage opportunity score using the provided calculator function
            arbitrage_score = calculator(ask_prices)
            
            if arbitrage_score > 1:
                # If the score indicates an arbitrage opportunity, print the score and the relevant ask prices
                print("Arbitrage Opportunity Score: {}".format(arbitrage_score))
                print(ask_prices)
            elif arbitrage_score == 1:
                # If the score is exactly 1, it indicates data might still be fetching; hence, wait
                print("Waiting for Binance API websocket data!")
            else:
                # If the score is below 1, no arbitrage opportunity is currently available
                print("No Arbitrage Opportunity yet! Score: {}".format(arbitrage_score))
            
            # Wait for 1 second before checking again to limit the rate of API calls and processing
            await asyncio.sleep(1)

def create_asset_pairs(coins, priority_coin='USDT'):
    """
    Generates trading pairs for the given list of coins, prioritizing pairs with a specified priority coin.

    Args:
        coins: A list of coin symbols.
        priority_coin: The coin to prioritize in pairing (default is 'USDT').

    Returns:
        list: A list of generated asset pairs.
    """
    assets = []
    
    # Create pairs combining each coin with the priority coin (e.g., 'BTCUSDT')
    for coin in coins:
        if coin != priority_coin:
            assets.append(coin + priority_coin)
    
    # Additionally, create pairs among the coins themselves, excluding the priority coin
    remaining_coins = [coin for coin in coins if coin != priority_coin]
    for i in range(len(remaining_coins)):
        for j in range(i + 1, len(remaining_coins)):
            # Note: This example appends reversed pairs; adjust according to your needs
            assets.append(remaining_coins[j] + remaining_coins[i])
    
    return assets

def parse_trading_pairs_from_text(text_content):
    """
    Parses a text content for trading pairs and formats them into a standardized list.

    Args:
        text_content (str): The raw text content containing trading pair information.

    Returns:
        list: A list of formatted trading pairs.
    """
    asset_pairs = []
    lines = text_content.split('\n')
    
    for line in lines:
        columns = line.split('\t')
        if len(columns) >= 3:
            trading_pairs_column = columns[2]
            trading_pairs = trading_pairs_column.split(';')
            for pair in trading_pairs:
                # Format each trading pair by removing '/' and spaces
                formatted_pair = pair.replace('/', '').replace(' ', '')
                if formatted_pair:
                    asset_pairs.append(formatted_pair)
                    
    return asset_pairs

def get_list_of_supported_pairs(file_path='List_of_Supported_Assets.txt'):
    """
    Reads a file containing a list of supported trading pairs and returns a formatted list.

    Args:
        file_path (str): The file path to the document containing trading pairs.

    Returns:
        list: A list of supported trading pairs formatted accordingly.
    """
    with open(file_path, 'r') as file:
        text_content = file.read()
    
    assets = parse_trading_pairs_from_text(text_content)
    return assets
