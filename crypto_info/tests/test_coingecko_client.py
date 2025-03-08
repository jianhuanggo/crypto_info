"""
Tests for the CoinGeckoClient class.
"""
import pytest
from unittest.mock import Mock, patch

from crypto_info.coingecko_client import CoinGeckoClient

class TestCoinGeckoClient:
    """Test cases for the CoinGeckoClient class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.client = CoinGeckoClient()
    
    @patch('crypto_info.api_client.APIClient._make_request')
    def test_get_coin_by_id(self, mock_make_request):
        """Test getting coin data by ID."""
        # Setup mock
        mock_make_request.return_value = {"id": "bitcoin", "name": "Bitcoin"}
        
        # Execute
        result = self.client.get_coin_by_id("bitcoin")
        
        # Verify
        mock_make_request.assert_called_once()
        assert result == {"id": "bitcoin", "name": "Bitcoin"}
    
    @patch('crypto_info.api_client.APIClient._make_request')
    def test_get_coin_price(self, mock_make_request):
        """Test getting coin price."""
        # Setup mock
        mock_make_request.return_value = {
            "bitcoin": {
                "usd": 50000,
                "eur": 42000
            }
        }
        
        # Execute
        result = self.client.get_coin_price(["bitcoin"], ["usd", "eur"])
        
        # Verify
        mock_make_request.assert_called_once()
        assert result == {"bitcoin": {"usd": 50000, "eur": 42000}}
        
        # Verify params
        args, kwargs = mock_make_request.call_args
        assert kwargs["params"]["ids"] == "bitcoin"
        assert kwargs["params"]["vs_currencies"] == "usd,eur"
    
    @patch('crypto_info.api_client.APIClient._make_request')
    def test_search_coins(self, mock_make_request):
        """Test searching for coins."""
        # Setup mock
        mock_make_request.return_value = {
            "coins": [
                {"id": "bitcoin", "name": "Bitcoin", "symbol": "btc"}
            ]
        }
        
        # Execute
        result = self.client.search_coins("bitcoin")
        
        # Verify
        mock_make_request.assert_called_once()
        assert result == {"coins": [{"id": "bitcoin", "name": "Bitcoin", "symbol": "btc"}]}
        
        # Verify params
        args, kwargs = mock_make_request.call_args
        assert kwargs["params"]["query"] == "bitcoin"
