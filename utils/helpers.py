import asyncio

async def check_arbitrage_opportunity(binance_ws, calculator, coins):
    while True:
        ask_prices = binance_ws.get_ask_prices(create_asset_pairs(coins))
        # print(ask_prices)
        if ask_prices:
            arbitrage_score = calculator(ask_prices)
            if(arbitrage_score > 1) :
                print("Arbitrage Opportunity Score: {}".format(arbitrage_score))
                print(ask_prices)
            elif (arbitrage_score == 1):
                print("Waiting for Binance API websocket data!")
            else:
                print("No Arbitrage Opportunity yet! Score: {}".format(arbitrage_score) )
            await asyncio.sleep(1)
        

def create_asset_pairs(coins, priority_coin ='USDT'):
    # Priority for pairing, assuming USDT is a common base or quote currency
    assets = []
    
    # Generate pairs where priority_coin is one of the currencies
    for coin in coins:
        if coin != priority_coin:
            assets.append(coin + priority_coin)
    
    # Generate pairs among the remaining coins excluding the priority_coin
    remaining_coins = [coin for coin in coins if coin != priority_coin]
    for i in range(len(remaining_coins)):
        for j in range(i + 1, len(remaining_coins)):
            # assets.append(remaining_coins[i] + remaining_coins[j])
            assets.append(remaining_coins[j] + remaining_coins[i])
    
    return assets


def parse_trading_pairs_from_text(text_content):
    """
    Parses trading pairs from the provided text content and creates a list of asset pairs.
    
    Args:
    text_content (str): Text content containing trading pairs information.
    
    Returns:
    list: A list of formatted asset pairs.
    """
    asset_pairs = []
    lines = text_content.split('\n')  # Splitting the text content into lines
    for line in lines:
        # Splitting each line by tabs or a significant number of spaces to get columns
        columns = line.split('\t')
        # Ensure the line has at least 3 columns (Asset, Networks, Trading Pairs)
        if len(columns) >= 3:
            # Extract the trading pairs column
            trading_pairs_column = columns[2]
            # Splitting trading pairs by ';' in case there are multiple pairs
            trading_pairs = trading_pairs_column.split(';')
            for pair in trading_pairs:
                # Removing any spaces and replacing '/' with '' to format pairs
                formatted_pair = pair.replace('/', '').replace(' ', '')
                if formatted_pair:  # Ensure the pair is not empty
                    asset_pairs.append(formatted_pair)
    return asset_pairs

# Example usage with the provided text content as a string variable `text_content`
# You would replace `text_content` with the actual content from your file

# Simulating reading the file (replace this part with actual file reading code)
def get_list_of_supported_pairs(file_path = 'List_of_Supported_Assets.txt'):
    with open(file_path, 'r') as file:
        text_content = file.read()

    assets = parse_trading_pairs_from_text(text_content)
    return assets
