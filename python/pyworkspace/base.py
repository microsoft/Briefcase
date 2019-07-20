import os
import re 
import yaml

from typing import Dict, List, TYPE_CHECKING
if TYPE_CHECKING:
    import pandas as pd
    import azureml.dataprep as dprep
    import pyspark.sql 

class Resource(yaml.YAMLObject):
    """The base class for resources referenced from resources.yaml
    """
    yaml_tag = u'!resource'
    
    # based on https://github.com/yaml/pyyaml/issues/266
    yaml_loader = yaml.SafeLoader

    def __init__(self, workspace=None, path=None, name: str=None):
        self.__workspace = workspace
        self.__path = path
        self.__name = name

    def get_params(self, *exclude: List[str]) -> Dict[str, str]:
        """Provides a list of configuration options provided by the user filtering out
           'exclude' parameters and internal attributes (e.g. prefixed with _)
        
        Args:
            exclude: list of attributes to exclude from parameters.

        Returns:
            Configuration options.
        """
        # TODO: filter credentialstore or change to _?
        return {k:v for k,v in self.__dict__.items()
                    if not (k.startswith('_') or k in exclude) }

    def get_credentials_providers(self):
        # TODO: the order of the providers
        # 1. silent ones (e.g. env/keyring/managed service identity? but it takes time to figure?)
        # 2. the specified one (e.g. device login)
        # 3. interactive fallback (e.g. prompt the user)

        # 1. check credentials attribute
        # 1a. find all credential stores (sort alphabetical)
        if hasattr(self, 'credentialstore'):
            return [self.credentialstore]
        else:
            from .credentialprovider import CredentialProvider, KeyRingCredentialProvider, EnvironmentCredentialProvider

            return [ # *self.get_workspace().get_all_of_type(CredentialProvider),
                    KeyRingCredentialProvider(),
                    EnvironmentCredentialProvider()]
                
    def get_name(self) -> str:
        return self._Workspace__name
    
    def get_path(self) -> List[str]:
        return self._Workspace__path

    def get_workspace(self) -> 'Workspace':
        return self._Workspace__workspace

    def get_secret(self, **kwargs) -> str:
        # rules to resolve
        # 3. resolve key by name
        # 3a. resolve key by path + name (. seperated)
        names = set([self.get_name(), '.'.join([*self.get_path(), self.get_name()])])

        providers = self.get_credentials_providers()

        # try all credential provides first
        for provider in providers:
            for key in names: 
                secret = provider.get_secret(key, **kwargs)

                if secret is not None:
                    return secret

        raise KeyNotFoundException("Secret not found for keys {} not found".format(names))

    def get_client(self):
        if not hasattr(self, 'client'):
            lazy_init = getattr(self, "get_client_lazy")
            if not callable(lazy_init):
                raise Exception("get_client_lazy must be a method")

            self.client = self.get_client_lazy()

        return self.client

class KeyNotFoundException(Exception):
    pass