import yaml
from azure.keyvault import KeyVaultClient, KeyVaultAuthentication, KeyVaultId
from ..credentialprovider import CredentialProvider

class AzureKeyVault(CredentialProvider):
    yaml_tag = u'!azure.keyvault'
    
    def __init__(self, dnsname, tenantid):
        self.dnsname = dnsname
        self.tenantid = tenantid

    def get_client(self):
        # cache the client
        if not hasattr(self, 'client'):
            # create a KeyVaultAuthentication instance which will callback to the supplied adal_callback
            credential_client = self.credential.get_client()

            # distinguish between serviceprincipal and adal callback auth
            auth = KeyVaultAuthentication(credential_client) if callable(credential_client) else credential_client 

            self.client = KeyVaultClient(auth)
        
        return self.client
        
    def get_secret(self, key, secret_version=KeyVaultId.version_none):
        # TODO: catch exception and rethrow CredentialProviderKeyNotFound
        return self.get_client().get_secret(self.dnsname, key, secret_version=secret_version).value