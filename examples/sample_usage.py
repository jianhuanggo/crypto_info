"""
Sample script demonstrating the usage of the crypto_info package.
"""
import logging
import sys
import json
from crypto_info import CryptoInfo

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger(__name__)

def print_crypto_details(symbol):
    """
    Print detailed information about a cryptocurrency.
    
    Args:
        symbol: Cryptocurrency symbol (e.g., 'BTC', 'ETH')
    """
    try:
        crypto_client = CryptoInfo()
        crypto_data = crypto_client.get_crypto_info(symbol)
        
        print(f"\n{'=' * 50}")
        print(f"Cryptocurrency Information: {crypto_data['name']} ({crypto_data['symbol']})")
        print(f"{'=' * 50}")
        
        # Basic information
        print(f"ID: {crypto_data['id']}")
        print(f"Market Cap Rank: {crypto_data['market_cap_rank']}")
        
        # Price information
        if 'usd' in crypto_data['current_price']:
            print(f"\nCurrent Price (USD): ${crypto_data['current_price']['usd']:,.2f}")
        if 'eur' in crypto_data['current_price']:
            print(f"Current Price (EUR): €{crypto_data['current_price']['eur']:,.2f}")
        if 'gbp' in crypto_data['current_price']:
            print(f"Current Price (GBP): £{crypto_data['current_price']['gbp']:,.2f}")
        
        # 24h price changes
        if crypto_data['price_change_24h'] is not None:
            print(f"\n24h Price Change: ${crypto_data['price_change_24h']:,.2f}")
        if crypto_data['price_change_percentage_24h'] is not None:
            print(f"24h Price Change (%): {crypto_data['price_change_percentage_24h']:,.2f}%")
        
        # Market data
        if 'usd' in crypto_data['market_cap']:
            print(f"\nMarket Cap (USD): ${crypto_data['market_cap']['usd']:,.2f}")
        if 'usd' in crypto_data['total_volume']:
            print(f"24h Trading Volume (USD): ${crypto_data['total_volume']['usd']:,.2f}")
        
        # 24h high/low
        if 'usd' in crypto_data['high_24h'] and 'usd' in crypto_data['low_24h']:
            print(f"\n24h High (USD): ${crypto_data['high_24h']['usd']:,.2f}")
            print(f"24h Low (USD): ${crypto_data['low_24h']['usd']:,.2f}")
        
        # Last updated
        print(f"\nLast Updated: {crypto_data['last_updated']}")
        
        print(f"{'=' * 50}\n")
        
    except Exception as e:
        logger.error(f"Error retrieving information for {symbol}: {e}")

def get_multiple_prices(symbols):
    """
    Get and print prices for multiple cryptocurrencies.
    
    Args:
        symbols: List of cryptocurrency symbols
    """
    try:
        crypto_client = CryptoInfo()
        
        print(f"\n{'=' * 50}")
        print("Cryptocurrency Prices")
        print(f"{'=' * 50}")
        
        for symbol in symbols:
            try:
                price_data = crypto_client.get_price(symbol)
                print(f"{symbol}:")
                if 'usd' in price_data:
                    print(f"  USD: ${price_data['usd']:,.2f}")
                if 'eur' in price_data:
                    print(f"  EUR: €{price_data['eur']:,.2f}")
                if 'gbp' in price_data:
                    print(f"  GBP: £{price_data['gbp']:,.2f}")
                print()
            except Exception as e:
                logger.error(f"Error retrieving price for {symbol}: {e}")
        
        print(f"{'=' * 50}\n")
        
    except Exception as e:
        logger.error(f"Error retrieving prices: {e}")

def main():
    """Main function to demonstrate the crypto_info package."""
    print("\nCrypto Info - Sample Usage\n")
    
    # Example 1: Get detailed information about Bitcoin
    print_crypto_details("BTC")
    
    # Example 2: Get detailed information about Ethereum
    print_crypto_details("ETH")
    
    # Example 3: Get detailed information about Solana
    print_crypto_details("SOL")
    
    # Example 4: Get detailed information about Raydium
    print_crypto_details("RAY")
    
    # Example 5: Get prices for multiple cryptocurrencies
    get_multiple_prices(["BTC", "ETH", "SOL", "RAY", "DOGE"])
    
    # Example 6: Handle invalid symbol
    try:
        crypto_client = CryptoInfo()
        crypto_data = crypto_client.get_crypto_info("INVALID_SYMBOL")
    except ValueError as e:
        print(f"Expected error for invalid symbol: {e}")

if __name__ == "__main__":
    main()
