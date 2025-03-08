"""
CoinGecko API client for fetching cryptocurrency data.
"""
import logging
from typing import Dict, Any, Optional, List
from .api_client import APIClient

logger = logging.getLogger(__name__)

class CoinGeckoClient(APIClient):
    """
    Client for interacting with the CoinGecko API.
    """
    def __init__(self, timeout: int = 30):
        """
        Initialize the CoinGecko API client.
        
        Args:
            timeout: Request timeout in seconds
        """
        super().__init__(base_url="https://api.coingecko.com/api/v3", timeout=timeout)
        
    def get_coin_by_id(self, coin_id: str, localization: bool = False, 
                      tickers: bool = False, market_data: bool = True,
                      community_data: bool = False, developer_data: bool = False,
                      sparkline: bool = False) -> Dict[str, Any]:
        """
        Get current data for a coin by its CoinGecko ID.
        
        Args:
            coin_id: CoinGecko ID of the coin (e.g., 'bitcoin', 'ethereum')
            localization: Include localized data
            tickers: Include ticker data
            market_data: Include market data
            community_data: Include community data
            developer_data: Include developer data
            sparkline: Include sparkline data
            
        Returns:
            Coin data as a dictionary
        """
        params = {
            'localization': str(localization).lower(),
            'tickers': str(tickers).lower(),
            'market_data': str(market_data).lower(),
            'community_data': str(community_data).lower(),
            'developer_data': str(developer_data).lower(),
            'sparkline': str(sparkline).lower()
        }
        
        return self._make_request(f"/coins/{coin_id}", params=params)
    
    def get_coin_price(self, coin_ids: List[str], vs_currencies: List[str],
                      include_market_cap: bool = False,
                      include_24hr_vol: bool = False,
                      include_24hr_change: bool = False,
                      include_last_updated_at: bool = False) -> Dict[str, Dict[str, float]]:
        """
        Get current price of coins in the specified currencies.
        
        Args:
            coin_ids: List of CoinGecko IDs of the coins
            vs_currencies: List of currencies to get prices in
            include_market_cap: Include market cap data
            include_24hr_vol: Include 24h volume data
            include_24hr_change: Include 24h price change data
            include_last_updated_at: Include last updated timestamp
            
        Returns:
            Dictionary of coin prices by currency
        """
        params = {
            'ids': ','.join(coin_ids),
            'vs_currencies': ','.join(vs_currencies),
            'include_market_cap': str(include_market_cap).lower(),
            'include_24hr_vol': str(include_24hr_vol).lower(),
            'include_24hr_change': str(include_24hr_change).lower(),
            'include_last_updated_at': str(include_last_updated_at).lower()
        }
        
        return self._make_request("/simple/price", params=params)
    
    def search_coins(self, query: str) -> Dict[str, Any]:
        """
        Search for coins, categories and markets listed on CoinGecko.
        
        Args:
            query: Search query
            
        Returns:
            Search results as a dictionary
        """
        params = {'query': query}
        return self._make_request("/search", params=params)
