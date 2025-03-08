"""
Main module for the crypto_info package.
"""
import logging
from typing import Dict, Any, Optional, List
from .coingecko_client import CoinGeckoClient

logger = logging.getLogger(__name__)

class CryptoInfo:
    """
    Main class for retrieving cryptocurrency information.
    """
    def __init__(self, api_client=None):
        """
        Initialize the CryptoInfo class.
        
        Args:
            api_client: Optional API client to use (defaults to CoinGeckoClient)
        """
        self.api_client = api_client or CoinGeckoClient()
        self._id_cache = {}  # Cache for symbol to ID mapping
        
    def _get_coin_id(self, symbol: str) -> str:
        """
        Get the CoinGecko ID for a cryptocurrency symbol.
        
        Args:
            symbol: Cryptocurrency symbol (e.g., 'BTC', 'ETH')
            
        Returns:
            CoinGecko ID for the symbol
            
        Raises:
            ValueError: If the symbol cannot be found
        """
        symbol = symbol.lower()
        
        # Check cache first
        if symbol in self._id_cache:
            return self._id_cache[symbol]
        
        # Search for the coin
        try:
            search_results = self.api_client.search_coins(symbol)
            coins = search_results.get('coins', [])
            
            # Find exact match for symbol
            for coin in coins:
                if coin.get('symbol', '').lower() == symbol:
                    self._id_cache[symbol] = coin.get('id')
                    return coin.get('id')
            
            # If no exact match, use the first result if available
            if coins:
                self._id_cache[symbol] = coins[0].get('id')
                logger.warning(f"No exact match for symbol '{symbol}', using '{coins[0].get('id')}'")
                return coins[0].get('id')
                
            raise ValueError(f"Could not find cryptocurrency with symbol '{symbol}'")
            
        except Exception as e:
            logger.error(f"Error finding coin ID for symbol '{symbol}': {e}")
            raise ValueError(f"Could not find cryptocurrency with symbol '{symbol}': {e}")
    
    def get_crypto_info(self, symbol: str) -> Dict[str, Any]:
        """
        Get detailed information about a cryptocurrency by its symbol.
        
        Args:
            symbol: Cryptocurrency symbol (e.g., 'BTC', 'ETH')
            
        Returns:
            Dictionary containing cryptocurrency information
            
        Raises:
            ValueError: If the symbol cannot be found
        """
        try:
            coin_id = self._get_coin_id(symbol)
            coin_data = self.api_client.get_coin_by_id(coin_id)
            
            # Extract relevant information
            result = {
                'id': coin_data.get('id'),
                'name': coin_data.get('name'),
                'symbol': coin_data.get('symbol', '').upper(),
                'description': coin_data.get('description', {}).get('en', ''),
                'image': coin_data.get('image', {}).get('large'),
                'current_price': {},
                'market_cap': {},
                'market_cap_rank': coin_data.get('market_cap_rank'),
                'total_volume': {},
                'high_24h': {},
                'low_24h': {},
                'price_change_24h': coin_data.get('market_data', {}).get('price_change_24h'),
                'price_change_percentage_24h': coin_data.get('market_data', {}).get('price_change_percentage_24h'),
                'last_updated': coin_data.get('last_updated')
            }
            
            # Extract price data for different currencies
            market_data = coin_data.get('market_data', {})
            for currency_field in ['current_price', 'market_cap', 'total_volume', 'high_24h', 'low_24h']:
                for currency, value in market_data.get(currency_field, {}).items():
                    result[currency_field][currency] = value
            
            return result
            
        except Exception as e:
            logger.error(f"Error getting information for symbol '{symbol}': {e}")
            raise ValueError(f"Failed to get information for cryptocurrency '{symbol}': {e}")
    
    def get_price(self, symbol: str, vs_currencies: List[str] = None) -> Dict[str, float]:
        """
        Get the current price of a cryptocurrency in various currencies.
        
        Args:
            symbol: Cryptocurrency symbol (e.g., 'BTC', 'ETH')
            vs_currencies: List of currencies to get prices in (defaults to ['usd', 'eur', 'gbp'])
            
        Returns:
            Dictionary of prices by currency
            
        Raises:
            ValueError: If the symbol cannot be found
        """
        if vs_currencies is None:
            vs_currencies = ['usd', 'eur', 'gbp']
        
        try:
            coin_id = self._get_coin_id(symbol)
            price_data = self.api_client.get_coin_price(
                [coin_id], 
                vs_currencies,
                include_24hr_change=True,
                include_market_cap=True
            )
            
            # Extract price data
            if coin_id in price_data:
                return price_data[coin_id]
            else:
                raise ValueError(f"No price data found for cryptocurrency '{symbol}'")
                
        except Exception as e:
            logger.error(f"Error getting price for symbol '{symbol}': {e}")
            raise ValueError(f"Failed to get price for cryptocurrency '{symbol}': {e}")
