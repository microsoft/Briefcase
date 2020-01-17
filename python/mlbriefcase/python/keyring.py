from ..credentialprovider import CredentialProvider

class KeyRingCredentialProvider(CredentialProvider):
    yaml_tag = u'!python.keyring'
    def get_secret(self, key, **kwargs):
        try:
            # conditional import
            import keyring

            # TODO: unclear if mlbriefcase is good value here
            # see https://pypi.org/project/keyring/#api-interface
            return keyring.get_password('mlbriefcase', key)
        except:
            return None
