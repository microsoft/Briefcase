from .base import *

class CredentialProvider(Resource):
    def get_secret(self, key, **kwargs):
        raise NotImplementedError

class AzureCredentialProvider(Resource):
    def get_secret(self, key, **kwargs):
        raise NotImplementedError
        # do it on databricks
        # return dbutils.notebook.entry_point.getDbutils().notebook().getContext().adlsAadToken().get() # 


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

class EnvironmentCredentialProvider(CredentialProvider):
    yaml_tag = u'!env'
    def get_secret(self, key, **kwargs):
        return os.environ.get(key)