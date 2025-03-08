# Crypto Info

A production-grade Python system for retrieving cryptocurrency information and current prices.

## Features

- Fetch detailed information about cryptocurrencies using their symbol (e.g., "BTC", "ETH", "RAY")
- Get current price data in various currencies
- Production-ready with error handling, logging, and comprehensive test coverage

## Installation

```bash
# Clone the repository
git clone https://github.com/jianhuanggo/crypto_info.git
cd crypto_info

# Install the package
pip install -e .

# Install development dependencies
pip install -e ".[dev]"
```

## Usage

```python
from crypto_info import CryptoInfo

# Initialize the client
crypto_client = CryptoInfo()

# Get information about a cryptocurrency by symbol
crypto_data = crypto_client.get_crypto_info("BTC")
print(f"Name: {crypto_data['name']}")
print(f"Symbol: {crypto_data['symbol']}")
print(f"Current Price (USD): ${crypto_data['current_price']['usd']}")

# Get only the price information
price_data = crypto_client.get_price("ETH")
print(f"ETH Price (USD): ${price_data['usd']}")
```

## Sample Script

Check out the `examples/sample_usage.py` script for a comprehensive demonstration of the package's capabilities:

```bash
# Run the sample script
python examples/sample_usage.py
```

## Development

### Testing

```bash
# Run tests
pytest
```

## API

The package uses the CoinGecko API to fetch cryptocurrency data. No API key is required for basic usage.

## License

MIT
