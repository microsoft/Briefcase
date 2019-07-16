from .base import *

class CredentialProvider(Resource):
    def get_secret(self, key, **kwargs):
        raise NotImplementedError

class CredentialNotFoundException(Exception):
    pass

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
            raise CredentialNotFoundException

class EnvironmentCredentialProvider(CredentialProvider):
    yaml_tag = u'!env'
    def get_secret(self, key, **kwargs):
        secret = os.environ.get(key)
        if secret is not None:
            return secret
        else:
            raise CredentialNotFoundException