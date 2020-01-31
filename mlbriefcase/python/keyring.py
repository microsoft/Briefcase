from ..credentialprovider import CredentialProvider

class keyring(CredentialProvider):
    def __init__(self):
        self.service_name = "mlbriefcase"

    def get_secret(self, key, **kwargs):
        try:
            # conditional import
            import keyring

            # see https://pypi.org/project/keyring/#api-interface
            return keyring.get_password(self.service_name, key)
        except:
            return None
