"""
Tests for the CryptoInfo class.
"""
import pytest
from unittest.mock import Mock, patch

from crypto_info.crypto_info import CryptoInfo

class TestCryptoInfo:
    """Test cases for the CryptoInfo class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_api_client = Mock()
        self.crypto_info = CryptoInfo(api_client=self.mock_api_client)
    
    def test_get_coin_id_from_cache(self):
        """Test getting coin ID from cache."""
        # Setup cache
        self.crypto_info._id_cache = {"btc": "bitcoin"}
        
        # Execute
        result = self.crypto_info._get_coin_id("BTC")
        
        # Verify
        assert result == "bitcoin"
        self.mock_api_client.search_coins.assert_not_called()
    
    def test_get_coin_id_exact_match(self):
        """Test getting coin ID with exact symbol match."""
        # Setup mock
        self.mock_api_client.search_coins.return_value = {
            "coins": [
                {"id": "bitcoin", "symbol": "btc"},
                {"id": "bitcoin-cash", "symbol": "bch"}
            ]
        }
        
        # Execute
        result = self.crypto_info._get_coin_id("BTC")
        
        # Verify
        assert result == "bitcoin"
        self.mock_api_client.search_coins.assert_called_once_with("btc")
        assert self.crypto_info._id_cache["btc"] == "bitcoin"
    
    def test_get_coin_id_no_exact_match(self):
        """Test getting coin ID with no exact symbol match."""
        # Setup mock
        self.mock_api_client.search_coins.return_value = {
            "coins": [
                {"id": "solana", "symbol": "sol"},
                {"id": "raydium", "symbol": "ray"}
            ]
        }
        
        # Execute
        result = self.crypto_info._get_coin_id("XYZ")
        
        # Verify
        assert result == "solana"
        self.mock_api_client.search_coins.assert_called_once_with("xyz")
        assert self.crypto_info._id_cache["xyz"] == "solana"
    
    def test_get_coin_id_no_results(self):
        """Test getting coin ID with no search results."""
        # Setup mock
        self.mock_api_client.search_coins.return_value = {"coins": []}
        
        # Execute and verify
        with pytest.raises(ValueError):
            self.crypto_info._get_coin_id("XYZ")
    
    def test_get_crypto_info(self):
        """Test getting cryptocurrency information."""
        # Setup mocks
        self.crypto_info._get_coin_id = Mock(return_value="bitcoin")
        self.mock_api_client.get_coin_by_id.return_value = {
            "id": "bitcoin",
            "name": "Bitcoin",
            "symbol": "btc",
            "description": {"en": "Bitcoin is a cryptocurrency."},
            "image": {"large": "https://example.com/bitcoin.png"},
            "market_data": {
                "current_price": {"usd": 50000, "eur": 42000},
                "market_cap": {"usd": 1000000000},
                "total_volume": {"usd": 50000000},
                "high_24h": {"usd": 52000},
                "low_24h": {"usd": 48000},
                "price_change_24h": 1000,
                "price_change_percentage_24h": 2.0
            },
            "market_cap_rank": 1,
            "last_updated": "2023-01-01T00:00:00Z"
        }
        
        # Execute
        result = self.crypto_info.get_crypto_info("BTC")
        
        # Verify
        self.crypto_info._get_coin_id.assert_called_once_with("BTC")
        self.mock_api_client.get_coin_by_id.assert_called_once_with("bitcoin")
        
        assert result["id"] == "bitcoin"
        assert result["name"] == "Bitcoin"
        assert result["symbol"] == "BTC"
        assert result["current_price"]["usd"] == 50000
        assert result["market_cap"]["usd"] == 1000000000
        assert result["price_change_24h"] == 1000
    
    def test_get_price(self):
        """Test getting cryptocurrency price."""
        # Setup mocks
        self.crypto_info._get_coin_id = Mock(return_value="bitcoin")
        self.mock_api_client.get_coin_price.return_value = {
            "bitcoin": {
                "usd": 50000,
                "eur": 42000,
                "gbp": 36000
            }
        }
        
        # Execute
        result = self.crypto_info.get_price("BTC")
        
        # Verify
        self.crypto_info._get_coin_id.assert_called_once_with("BTC")
        self.mock_api_client.get_coin_price.assert_called_once()
        
        assert result["usd"] == 50000
        assert result["eur"] == 42000
        assert result["gbp"] == 36000
