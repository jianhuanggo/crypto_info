"""
API client for interacting with cryptocurrency data providers.
"""
import logging
from typing import Dict, Any, Optional, List
import requests
from requests.exceptions import RequestException, Timeout, HTTPError

logger = logging.getLogger(__name__)

class APIClient:
    """
    Base API client for making HTTP requests to cryptocurrency data providers.
    """
    def __init__(self, base_url: str, timeout: int = 30):
        """
        Initialize the API client.
        
        Args:
            base_url: Base URL for the API
            timeout: Request timeout in seconds
        """
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()
    
    def _make_request(self, endpoint: str, method: str = "GET", 
                     params: Optional[Dict[str, Any]] = None,
                     headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Make an HTTP request to the API.
        
        Args:
            endpoint: API endpoint to call
            method: HTTP method (GET, POST, etc.)
            params: Query parameters
            headers: HTTP headers
            
        Returns:
            API response as a dictionary
            
        Raises:
            ValueError: If the API returns an error
            ConnectionError: If there's a network issue
            Timeout: If the request times out
            HTTPError: If the API returns a non-200 status code
        """
        url = f"{self.base_url}{endpoint}"
        
        try:
            logger.debug(f"Making {method} request to {url} with params: {params}")
            
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                headers=headers,
                timeout=self.timeout
            )
            
            response.raise_for_status()
            
            return response.json()
            
        except Timeout:
            logger.error(f"Request to {url} timed out after {self.timeout} seconds")
            raise Timeout(f"Request to {url} timed out")
            
        except HTTPError as e:
            logger.error(f"HTTP error: {e}")
            
            # For HTTPError from requests, the response might be available
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Status code: {e.response.status_code}")
                
                # Try to get error details from response
                error_detail = ""
                try:
                    error_detail = e.response.json()
                except ValueError:
                    error_detail = e.response.text
                    
                raise HTTPError(f"API error: {error_detail}", response=e.response)
            else:
                # Re-raise the original exception if no response is available
                raise
            
        except RequestException as e:
            logger.error(f"Request error: {e}")
            raise ConnectionError(f"Failed to connect to {url}: {e}")
            
        except ValueError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            raise ValueError(f"Invalid response format: {e}")
