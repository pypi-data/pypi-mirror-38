"""
`BlobStorage` class.
"""
import asyncio

from .exceptions import (BlobStorageMissingCredentialsError,
                         BlobStorageUnrecognizedProviderError, )
from .providers import (Backblaze, ProviderAuthenticationError,
                        ProviderFileUploadError, PROVIDERS, )


class BlobStorage:
    """
    Asynchronous object storage interface for common operations, e.g.
    uploading a file to a bucket.

    Providers currently supported:

    Backblaze.
    """
    PROVIDER_ADAPTER = {
        'backblaze': {
            'adapter': Backblaze,
            'required': ('account_id', 'app_key'),
        }
    }

    def __init__(self, provider, **kwargs):
        r"""
        Set the object storage provider and the event loop.

        :param str provider: Name of the object storage provider. Must be one
               of `'backblaze'`.
        :param \**kwargs: Credentials for the object storage provider, see
               below.

        : Keyword arguments:
            * *account_id* (``str``) --
              Account id (Backblaze).
            * *app_key* (``str``) --
              Application key (Backblaze).

        .. automethod:: _upload_file
        """
        if provider not in PROVIDERS:
            raise BlobStorageUnrecognizedProviderError
        if not all(r in kwargs
                   for r in self.PROVIDER_ADAPTER[provider]['required']):
            raise BlobStorageMissingCredentialsError
        self.provider = self.PROVIDER_ADAPTER[provider]['adapter'](**kwargs)
        self.loop = asyncio.get_event_loop()

    async def _upload_file(self, bucket_id, file_to_upload):
        """
        Upload a single file to the object storage provider.

        :param str bucket_id: Object storage provider bucket to upload files
               to.
        :param dict file_to_upload: Local file to upload,
               `{'path': str, 'content_type': str}`.
        :raise ProviderAuthenticationError: If authentication to the object
               storage provider is unsuccessful.
        :raise ProviderFileUploadError: If uploading of the file to the object
               storage provider bucket is unsuccessful.
        :return: Response from object storage provider.
        :rtype: ``dict``
        """
        auth_response = await self.provider.authenticate()
        if not auth_response:
            raise ProviderAuthenticationError
        upload_file_response = await self.provider.upload_file(
            bucket_id, file_to_upload['path'], file_to_upload['content_type'])
        if not upload_file_response:
            raise ProviderFileUploadError
        return upload_file_response

    def upload_files(self, bucket_id, files_to_upload):
        """
        Upload multiple files to the object storage provider.

        :param str bucket_id: Object storage provider bucket to upload files
               to.
        :param list files_to_upload: Files to upload; each file is a `dict`,
               `{'path': str, 'content_type': str}`.
        :return: Some value
        :rtype: ``dict``
        """
        async def _upload_files():
            futures = []
            for file_to_upload in files_to_upload:
                future = asyncio.ensure_future(
                    self._upload_file(bucket_id, file_to_upload))
                futures.append(future)
            return await asyncio.gather(*futures)
        return self.loop.run_until_complete(_upload_files())
