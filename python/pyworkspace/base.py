import yaml
import os
import re 

from typing import List, TYPE_CHECKING
if TYPE_CHECKING:
    import pandas as pd
    import azureml.dataprep as dprep
    import pyspark.sql 

class Resource(yaml.YAMLObject)
    """The base class for resources referenced from resources.yaml
    """

    def __init__(self, workspace=None, path=None, name=None):
        self.__workspace = workspace
        self.__path = path
        self.__name = name

    def get_params(self, *exclude: Map[str, str]):
        """Provides a list of configuration options provided by the user filtering out
           'exclude' parameters and internal attributes (e.g. prefixed with _)
        
        Returns:
            Map[str, str] -- Configuration options.
        """
        # TODO: filter credentialstore or change to _?
        return {k:v for k,v in self.__dict__.items()
                    if not (k.startswith('_') or k in exclude) }

    def get_credentials_providers(self):
        # 1. check credentials attribute
        # 1a. find all credential stores (sort alphabetical)
        if hasattr(self, 'credentialstore'):
            return [self.credentialstore]
        else:
            from .credentialprovider import CredentialProvider, KeyRingCredentialProvider, EnvironmentCredentialProvider

            return [*self.get_workspace().get_all_of_type(CredentialProvider),
                    KeyRingCredentialProvider(),
                    EnvironmentCredentialProvider()]
                
    def get_name(self) -> str:
        return self._Workspace__name
    
    def get_path(self) -> List[str]:
        return self._Workspace__path

    def get_workspace(self) -> 'Workspace':
        return self._Workspace__workspace

    def get_secret(self, **kwargs):
        # rules to resolve
        # 3. resolve key by name
        # 3a. resolve key by path + name (. seperated)
        names = [self.get_name(), '.'.join([*self.get_path(), self.get_name()])]

        providers = self.get_credentials_providers()

        # try all credential provides first
        for provider in providers:
            for key in names: 
                try:
                    return provider.get_secret(key, **kwargs)
                except CredentialNotFoundException:
                    pass

        raise CredentialNotFoundException
