import os
import re
import yaml

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

    def update_child(self, child):
        child.__workspace = self.__workspace
        child.__names = self.__names
        # TODO: probably searching up the path is a better choice?
        if hasattr(self, 'credentialstore'):
            child.credentialstore = self.credentialstore

    def add_name(self, workspace, path, name: str):
        self.__workspace = workspace

        if not hasattr(self, '_Resource__names'):
            self.__names = set()

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
        if hasattr(self, 'credentialstore') and self.credentialstore is not None:
            return [self.credentialstore]
        else:
            from .credentialprovider import CredentialProvider, EnvironmentCredentialProvider
            from .python.keyring import KeyRingCredentialProvider
            from .python.jupyterlab_credentialstore import JupyterLabCredentialStore

            return [  # *self.get_workspace().get_all_of_type(CredentialProvider),
                JupyterLabCredentialStore(),
                KeyRingCredentialProvider(),
                EnvironmentCredentialProvider()]

    def get_names(self) -> Set[str]:
        return self.__names

    def get_workspace(self) -> 'Workspace':
        return self.__workspace

    def get_secret(self, **kwargs) -> str:
        # rules to resolve
        # 3. resolve key by name
        # 3a. resolve key by path + name (. seperated)

        providers = self.get_credentials_providers()
        names = self.get_names()

        # try all credential provides first
        for provider in providers:
            for key in names:
                # print("Probing for secret: {} {}".format(provider, key))
                secret = provider.get_secret(key, **kwargs)

                if secret is not None:
                    return secret

        raise KeyNotFoundException(
            "Secret not found for keys {} not found".format(names))

    def get_client(self):
        if not hasattr(self, 'client'):
            lazy_init = getattr(self, "get_client_lazy")
            if not callable(lazy_init):
                raise Exception("get_client_lazy must be a method")

            self.client = self.get_client_lazy()

        return self.client


class KeyNotFoundException(Exception):
    pass
