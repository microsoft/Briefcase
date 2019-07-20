# TODO. headers, comments
import yaml
from enum import Enum
import datetime
# TODO: from workspace.base import ... should work
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

    def is_secret_a_sas_token(self) -> bool:
        return self.get_secrettype().lower() == 'sas'

    def get_client_lazy(self):
        # only import if method is used
        from azure.storage.common import CloudStorageAccount
        
        # key vs SAS token
        account_key = sas_token = None
        if self.is_secret_a_sas_token():
            sas_token = self.get_secret()
        else:
            account_key = self.get_secret()
        
        # TODO: endpoint_suffix
        return CloudStorageAccount(account_name=self.accountname,
                                            account_key=account_key,
                                            sas_token=sas_token,
                                            is_emulated=getattr(self, "is_emulated", None),
                                            endpoint_suffix=getattr(self, "endpoint_suffix", None))

class AzureBlob(URLDataSource):
    yaml_tag = u'!azure.blob'
    def __init__(self, datasource, path):
        self.datasource = datasource
        self.path = path

    def download(self, target) -> None:
        block_blob_service = self.datasource.get_client().create_block_blob_service()
        block_blob_service.get_blob_to_path(self.container_name, target, self.path)

    def get_url(self) -> str:
        if not hasattr(self, 'datasource'):
            raise Exception("requires azure storage account as data source")

        if self.datasource.is_secret_a_sas_token():
            sas_token = self.datasource.get_secret()
        else:
            from azure.storage.blob.sharedaccesssignature import BlobSharedAccessSignature
            from azure.storage.blob.models import ContainerPermissions

            # could also get SAS on the fly by getting ADAL context: https://github.com/Azure/azure-storage-python/blob/master/azure-storage-blob/azure/storage/blob/sharedaccesssignature.py
            sas = BlobSharedAccessSignature(self.datasource.accountname, account_key=self.datasource.get_secret())

            now = datetime.datetime.utcnow()
            sas_token = sas.generate_blob(
                self.containername, 
                self.path,
                permission=ContainerPermissions(read=True), # TODO: maybe write?
                start=now - datetime.timedelta(hours=1), # this feels like trouble
                expiry=now + datetime.timedelta(hours=12))

        # TODO: secure vs non-secure
        # other clouds
        # TODO: urllib has path join method including encoding
        return "https://{}.blob.core.windows.net/{}/{}?{}".format(
            self.datasource.accountname,
            self.containername,
            self.path,
            sas_token)