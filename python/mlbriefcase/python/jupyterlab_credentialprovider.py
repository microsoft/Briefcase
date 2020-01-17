from ..credentialprovider import CredentialProvider

# https://towardsdatascience.com/the-jupyterlab-credential-store-9cc3a0b9356 
class JupyterLabCredentialProvider(CredentialProvider):
    yaml_tag = u'!python.jupyter.credentialprovider'
    def get_secret(self, key, **kwargs):
        try:
            import kernel_connector as kc

            return kc.get_credential(key)
        except:
            return None
