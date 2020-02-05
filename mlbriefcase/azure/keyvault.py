from azure.keyvault import KeyVaultClient, KeyVaultAuthentication, KeyVaultId
from azure.keyvault.models import KeyVaultErrorException
from ..credentialprovider import CredentialProvider

class keyvault(CredentialProvider):
    pip_package = 'azure-keyvault==1.1.0'

    def get_client_lazy(self):
        # create a KeyVaultAuthentication instance which will callback to the supplied adal_callback
        credential_client = self.get_briefcase()[self.credential].get_client()

        # distinguish between serviceprincipal and adal callback auth
        auth = KeyVaultAuthentication(credential_client) if callable(
            credential_client) else credential_client

        return KeyVaultClient(auth)

    def get_secret(self, key, secret_version=KeyVaultId.version_none):
        try:
            return self.get_client().get_secret(self.dnsname, key, secret_version=secret_version).value
        except KeyVaultErrorException as ex:
            return None
