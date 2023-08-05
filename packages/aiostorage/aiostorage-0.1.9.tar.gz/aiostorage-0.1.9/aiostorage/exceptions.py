"""
Exceptions for errors whilst using the `BlobStorage` class.
"""
from .providers import PROVIDERS


class BlobStorageError(Exception):
    """
    Base exception class.
    """


class BlobStorageUnrecognizedProviderError(BlobStorageError):
    """
    Unrecognized object storage provider.
    """
    def __str__(self):
        return ('Unrecognized object storage provider. Please select one of'
                f' {", ".join(PROVIDERS)}')


class BlobStorageMissingCredentialsError(BlobStorageError):
    """
    Missing credentials for authenticating to object storage provider.
    """
    def __str__(self):
        return ('Missing credentials for authenticating to object storage '
                'provider')
