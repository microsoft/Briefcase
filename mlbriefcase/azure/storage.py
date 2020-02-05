# TODO. headers, comments
import yaml
from enum import Enum
import datetime
from ..base import KeyNotFoundException
from ..datasource import URLDataSource
from .azure_resource import AzureResource

class account(AzureResource):
    pip_package = 'azure-storage-blob'

    def __init__(self):
        self.secrettype = 'key'

    def is_secret_a_sas_token(self) -> bool:
        return self.secrettype == 'sas'

    def get_secret(self):
        # TODO: cache secret
        try:
            return super().get_secret()
        except KeyNotFoundException as ex:
            try:
                from azure.mgmt.storage import StorageManagementClient

                auth_client = self.get_auth_client()

                resource_group = self.get_resource_group()

                # loop through subscriptions
                for sub in self.get_subscriptions():
                    for id in sub.get_ids():
                        self.get_logger().debug("secret probing: searching Azure subscription '{}' for azure storage account '{}'".format(id, self.accountname))
                        storage_client = StorageManagementClient(
                            auth_client.get_client(), id)

                        if resource_group is None:
                            for acc in storage_client.storage_accounts.list():
                                if acc.name == self.accountname:
                                    # found the account, let's break out
                                    resource_group = acc.id.split('/')[4]
                                    break

                            # let's check if we found the account, if not let's try the next subscription
                            if resource_group is None:
                                continue

                        self.get_logger().debug("secret found:  Azure storage account '{}' in resource group '{}'".format(self.accountname, resource_group))
                        storage_keys = storage_client.storage_accounts.list_keys(
                            resource_group, self.accountname)
                        # TODO: this seems to be model dependent?
                        return storage_keys.keys[0].value
            except Exception as e:
                raise e

    def get_client_lazy(self):
        # only import if method is used
        from azure.storage.common import CloudStorageAccount

        # key vs SAS token
        account_key = sas_token = None

        try:
            if self.is_secret_a_sas_token():
                sas_token = self.get_secret()
            else:
                account_key = self.get_secret()
        except KeyNotFoundException as e:
            # fallback to subscription lookup
            account_key = self._find_key_through_subscription()

            if account_key is None:
                raise e

        # TODO: endpoint_suffix
        return CloudStorageAccount(account_name=self.accountname,
                                   account_key=account_key,
                                   sas_token=sas_token,
                                   is_emulated=getattr(
                                       self, "is_emulated", None),
                                   endpoint_suffix=getattr(self, "endpoint_suffix", None))


class blob(URLDataSource):
    pip_package = 'azure-storage-blob'

    def download(self, target) -> None:
        datasource = self.get_briefcase()[self.account]
        block_blob_service = datasource.get_client().create_block_blob_service()
        block_blob_service.get_blob_to_path(
            self.containername, target, self.path)

    def get_url(self) -> str:
        if hasattr(self, 'account'):
            self.datasource = self.get_briefcase()[self.account]
        else:
            if not hasattr(self, 'url'):
                raise Exception(
                    "requires azure storage account as data source")

            import urllib.parse

            components = urllib.parse.urlparse(self.url)

            # TODO: http/https
            hostAndPort = components.netloc.split(':')

            # support other azure clouds (public, gov, ...)
            accountname = hostAndPort[0].split('.')[0]

            self.datasource = account()
            self.datasource.accountname = accountname
            self.update_child(self.datasource)

            path = components.path.split('/')
            self.containername = path[1]
            self.path = str.join('/', path[2:])

        if self.datasource.is_secret_a_sas_token():
            sas_token = self.datasource.get_secret()
        else:
            from azure.storage.blob import generate_blob_sas, BlobSasPermissions

            # could also get SAS on the fly by getting ADAL context: https://github.com/Azure/azure-storage-python/blob/master/azure-storage-blob/azure/storage/blob/sharedaccesssignature.py
            now = datetime.datetime.utcnow()
            sas_token = generate_blob_sas(
                self.datasource.accountname,
                self.containername,
                self.path,
                account_key=self.datasource.get_secret(),
                permission=BlobSasPermissions(read=True),
                expiry=now + datetime.timedelta(hours=12))

        # TODO: secure vs non-secure
        # other clouds
        # TODO: urllib has path join method including 
        return "https://{}.blob.core.windows.net/{}/{}?{}".format(
            self.datasource.accountname,
            self.containername,
            self.path,
            sas_token)