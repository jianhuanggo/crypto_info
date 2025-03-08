"""
Tests for the APIClient class.
"""
import pytest
from unittest.mock import Mock, patch
import requests
from requests.exceptions import Timeout, HTTPError, RequestException

from crypto_info.api_client import APIClient

class TestAPIClient:
    """Test cases for the APIClient class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.client = APIClient(base_url="https://test-api.com")
    
    @patch('requests.Session.request')
    def test_make_request_success(self, mock_request):
        """Test successful API request."""
        # Setup mock
        mock_response = Mock()
        mock_response.json.return_value = {"data": "test_data"}
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response
        
        # Execute
        result = self.client._make_request("/test-endpoint", params={"param": "value"})
        
        # Verify
        mock_request.assert_called_once_with(
            method="GET",
            url="https://test-api.com/test-endpoint",
            params={"param": "value"},
            headers=None,
            timeout=30
        )
        assert result == {"data": "test_data"}
    
    @patch('requests.Session.request')
    def test_make_request_timeout(self, mock_request):
        """Test API request timeout."""
        # Setup mock
        mock_request.side_effect = Timeout("Request timed out")
        
        # Execute and verify
        with pytest.raises(Timeout):
            self.client._make_request("/test-endpoint")
    
    @patch('requests.Session.request')
    def test_make_request_http_error(self, mock_request):
        """Test API request HTTP error."""
        # Setup mock
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = HTTPError("404 Client Error")
        mock_response.status_code = 404
        mock_response.json.return_value = {"error": "Not found"}
        mock_request.return_value = mock_response
        
        # Execute and verify
        with pytest.raises(HTTPError):
            self.client._make_request("/test-endpoint")
    
    @patch('requests.Session.request')
    def test_make_request_connection_error(self, mock_request):
        """Test API request connection error."""
        # Setup mock
        mock_request.side_effect = RequestException("Connection error")
        
        # Execute and verify
        with pytest.raises(ConnectionError):
            self.client._make_request("/test-endpoint")
    
    @patch('requests.Session.request')
    def test_make_request_json_error(self, mock_request):
        """Test API request JSON parsing error."""
        # Setup mock
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_request.return_value = mock_response
        
        # Execute and verify
        with pytest.raises(ValueError):
            self.client._make_request("/test-endpoint")
