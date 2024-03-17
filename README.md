# Triangular Arbitrage in Cryptocurrency Markets

This project implements a basic framework for identifying potential triangular arbitrage opportunities in real-time cryptocurrency markets using the Binance WebSocket API. It monitors selected cryptocurrency pairs for price updates and calculates the possibility of triangular arbitrage.

## Features

- Real-time data fetching from Binance WebSocket API.
- Supports multiple cryptocurrency pairs for arbitrage calculation.
- Dynamically checks for triangular arbitrage opportunities among a set of assets.
- Easy to extend and customize for different assets or additional strategies.
- Includes a `ArbitrageCalculator` class for evaluating arbitrage opportunities based on the latest market data.
- Utilizes asynchronous programming for efficient real-time data handling.

## Requirements

- Python 3.6+
- `websockets`
- `asyncio`
- Access to the internet and ability to connect to Binance API services.

## Installation

1. Ensure Python 3.6 or higher is installed on your system.
2. Install the required Python packages:

```bash
pip install websockets asyncio
```

3. Clone this repository or download the source code.

## Usage

To run the arbitrage monitor, execute the `main.py` script from the terminal:

```bash
python main.py
```

By default, the script is configured to monitor a predefined set of cryptocurrency pairs. You can modify the `assets` list in `main.py` to include the pairs you are interested in.

## Structure

- `BinanceWebSocket.py`: Contains the `BinanceWebSocket` class for connecting to the Binance WebSocket API and fetching real-time price data.
- `ArbitrageCalculator.py`: Contains the `ArbitrageCalculator` class for calculating potential triangular arbitrage opportunities.
- `main.py`: The main entry point of the application. Initializes the WebSocket connection and periodically checks for arbitrage opportunities.
- Helper functions for asset pair creation and data parsing are included to enhance flexibility and ease of use.

## Customization

You can customize the list of cryptocurrency pairs to monitor by editing the `assets` list in `main.py`. The `ArbitrageCalculator` class can be extended to include more sophisticated arbitrage calculation strategies or to factor in transaction fees and slippage.

## Disclaimer

This project is for educational purposes only. Cryptocurrency trading involves significant risk, and you should perform your own due diligence before trading. The authors of this project are not responsible for any financial losses incurred by using this software.

## Contributions

Contributions are welcome! Please submit a pull request or open an issue if you have suggestions for improvements or have identified bugs.

## License

This project is licensed under the MIT License - see the LICENSE file for details.