"""
Crypto Info package for retrieving cryptocurrency information and prices.
"""
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

from .crypto_info import CryptoInfo

__all__ = ['CryptoInfo']
