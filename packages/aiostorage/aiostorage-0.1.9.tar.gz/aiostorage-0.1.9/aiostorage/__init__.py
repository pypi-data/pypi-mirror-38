"""
API for public consumption.

Example usage:

.. highlight:: python
.. code-block:: python

    from aiostorage import BlobStorage

    file1 = {'content': 'application/pdf', 'path': '/path/to/pdf'}
    file2 = {'content': 'video/mp4', 'path': '/path/to/video'}
    storage = BlobStorage('backblaze', app_key='key8923', account_id='234234')
    storage.upload_files('bucket-1234', [file1, file2])
"""
from .blob_storage import BlobStorage
from .exceptions import (BlobStorageMissingCredentialsError,
                         BlobStorageUnrecognizedProviderError,)

__version__ = '0.1.9'

__all__ = ['BlobStorage', 'BlobStorageUnrecognizedProviderError',
           'BlobStorageMissingCredentialsError']
