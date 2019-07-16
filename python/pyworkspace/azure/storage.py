# TODO. headers, comments
import yaml
from enum import Enum
from ..base import Resource
from ..datasource import URLDataSource

class AzureStorage(Resource):
    yaml_tag = u'!azure.storage'
    def __init__(self, accountname, accountkey=None, credentialstore=None):
        self.accountname = accountname
        self.accountkey = accountkey
        self.credentialstore = credentialstore

    def get_secrettype(self) -> str:
        if not hasattr(self, 'secrettype'):
            self.secrettype = 'key'

        return self.secrettype

    def get_client(self):
        if not hasattr(self, 'client'):
            # only import if method is used
            from azure.storage.common import CloudStorageAccount
            
            # key vs SAS token
            account_key = sas_token = None
            if self.get_secrettype().lower() == 'sas':
                sas_token = self.get_secret()
            else:
                account_key = self.get_secret()
            
            # TODO: endpoint_suffix
            self.client = CloudStorageAccount(account_name=self.accountname,
                                              account_key=account_key,
                                              sas_token=sas_token,
                                              is_emulated=self.__dict__.get("is_emulated", None),
                                              endpoint_suffix=self.__dict__.get("endpoint_suffix", None))
        
        return self.client

class AzureBlob(URLDataSource):
    yaml_tag = u'!azure.blob'
    def __init__(self, datasource, path):
        self.datasource = datasource
        self.path = path

    def download(self, target) -> None:
        block_blob_service = self.datasource.get_client().create_block_blob_service()
        block_blob_service.get_blob_to_path(self.container_name, target, self.path)

    def get_url(self) -> str:
        # append SAS token
        # if SAS not there, create one       
        pass