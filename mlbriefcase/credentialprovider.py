from .base import *
import os

class CredentialProvider(Resource):
    def get_secret(self, key, **kwargs):
        raise NotImplementedError


class AzureCredentialProvider(Resource):
    def get_secret(self, key, **kwargs):
        raise NotImplementedError
        # do it on databricks
        # return dbutils.notebook.entry_point.getDbutils().notebook().getContext().adlsAadToken().get() #


class EnvironmentCredentialProvider(CredentialProvider):
    yaml_tag = u'!env'

    def get_secret(self, key, **kwargs):
        return os.environ.get(key.replace('.', '_'))

class DotEnvCredentialProvider(CredentialProvider):
    def __init__(self, env):
        self.env = env

    def get_secret(self, key, **kwargs):
        return self.env[key] if key in self.env else None
