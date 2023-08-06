from azure.storage.blob.blockblobservice import BlockBlobService
from azure.storage.file.fileservice import FileService
import os


class AzureCredentials:

    _account_name = os.environ.get('azure_account_name')
    _account_key = os.environ.get('azure_account_key')

    def __init__(self, account_name=None, account_key=None):

        self.account_name = account_name if account_name else AzureCredentials._account_name
        self.account_key = account_key if account_key else AzureCredentials._account_key

    def get_blob_service(self):

        return BlockBlobService(
            account_name=self.account_name,
            account_key=self.account_key
        )

    def get_file_service(self):

        return FileService(
            account_name=self.account_name,
            account_key=self.account_key
        )
