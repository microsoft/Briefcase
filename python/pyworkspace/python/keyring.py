from ..credentialprovider import CredentialProvider

class KeyRingCredentialProvider(CredentialProvider):
    yaml_tag = u'!python.keyring'
    def get_secret(self, key, **kwargs):
        try:
            # conditional import
            import keyring

            # TODO: unclear if pyworkspace is good value here
            # see https://pypi.org/project/keyring/#api-interface
            return keyring.get_password('pyworkspace', key)
        except:
            return None
