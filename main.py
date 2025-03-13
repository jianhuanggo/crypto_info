def example():
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

    # Get only the price information
    price_data = crypto_client.get_price("RAY")
    print(f"RAY Price (USD): ${price_data['usd']}")

    # Get only the price information
    price_data = crypto_client.get_price("RAY")
    print(f"RAY Price (USD): ${price_data['usd']}")

    # Get only the price information
    price_data = crypto_client.get_price("VIRTUAL")
    print(f"VIRTUAL Price (USD): ${price_data['usd']}")

def main(symbol: str) -> dict:
    import _json

    from crypto_info import CryptoInfo

    # Initialize the client

    return CryptoInfo().get_price(symbol)


if __name__ == "__main__":
    print(main("VIRTUAL"))
