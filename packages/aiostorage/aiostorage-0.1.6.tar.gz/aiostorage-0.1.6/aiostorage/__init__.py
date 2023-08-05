"""
API for public consumption.
"""
from .blob_storage import BlobStorage
from .exceptions import BlobStorageUnrecognizedProviderError

__version__ = '0.1.6'

__all__ = ['BlobStorage', 'BlobStorageUnrecognizedProviderError']
