import os
import re
import yaml
import logging

from typing import Dict, List, Set, TYPE_CHECKING
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

    def get_logger(self):
        return self.__logger

    def update_child(self, child):
        child.init(self.__workspace, '', '')
        
        child.__names = self.__names
        # TODO: probably searching up the path is a better choice?
        child.credentialstore = self.credentialstore
            
        return child

    def init(self, workspace, path, name: str):
        # avoid duplicate initialize
        if '_Resource__workspace' in self.__dict__:
            return

        self.__logger = logging.getLogger('workspace')
        self.__names = set()
        self.__client = None

        self.__workspace = workspace

        self.__names.add(name)
        self.__names.add('.'.join([*path, name]))

    def get_params(self, *exclude: List[str]) -> Dict[str, str]:
        """Provides a list of configuration options provided by the user filtering out
           'exclude' parameters and internal attributes (e.g. prefixed with _)

        Args:
            exclude: list of attributes to exclude from parameters.

        Returns:
            Configuration options.
        """
        # TODO: filter credentialstore or change to _?
        return {k: v for k, v in self.__dict__.items()
                if not (k.startswith('_') or k in exclude)}

    def get_credentials_providers(self):
        # TODO: the order of the providers
        # 1. silent ones (e.g. env/keyring/managed service identity? but it takes time to figure?)
        # 2. the specified one (e.g. device login)
        # 3. interactive fallback (e.g. prompt the user)

        # 1. check credentials attribute
        # 1a. find all credential stores (sort alphabetical)
        if 'credentialstore' in self.__dict__:
            return [self.credentialstore]
        else:
            from .credentialprovider import CredentialProvider, EnvironmentCredentialProvider, DotEnvCredentialProvider
            from .python.keyring import KeyRingCredentialProvider
            from .python.jupyterlab_credentialstore import JupyterLabCredentialStore

            return [  # *self.get_workspace().get_all_of_type(CredentialProvider),
                JupyterLabCredentialStore(),
                KeyRingCredentialProvider(),
                EnvironmentCredentialProvider(),
                DotEnvCredentialProvider(self.get_workspace().get_env())]

    def get_names(self) -> Set[str]:
        return self.__names

    def get_workspace(self) -> 'Workspace':
        return self.__workspace

    def get_secret(self, **kwargs) -> str:
        return self.__get_secret(self.get_names(), **kwargs)

    def __get_secret(self, names: List[str], **kwargs) -> str:
        # rules to resolve
        # 3. resolve key by name
        # 3a. resolve key by path + name (. seperated) 

        providers = self.get_credentials_providers()    

        # try all credential provides first
        for provider in providers:
            for key in names:
                self.get_logger().debug("secret probing: {} for {} ...".format(provider.__class__.__name__, key))
                secret = provider.get_secret(key, **kwargs)

                if secret is not None:
                    self.get_logger().debug("secret found:  {} {}".format(provider.__class__.__name__, key))
                    return secret

        raise KeyNotFoundException(
            "Secret not found for keys {} not found".format(names))

    def __getattr__(self, name):
        # print('__getattr__ {}'.format(name))

        # used by pyyaml
        if name == '__setstate__':
            raise AttributeError()

        try:
            return self.__get_secret(list(map(lambda n: '{}.{}'.format(n, name), self.get_names())))
        except KeyNotFoundException:
            raise AttributeError()

    # used for test injection
    def set_client(self, client):
        self.__client = client

    def get_client(self):
        if self.__client is None:
            lazy_init = getattr(self, "get_client_lazy")
            if not callable(lazy_init):
                raise Exception("get_client_lazy must be a method")

            self.__client = self.get_client_lazy()

        return self.__client


class KeyNotFoundException(Exception):
    pass
