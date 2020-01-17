import os
import re
import yaml
import logging
import timeit

from typing import Dict, List, Set, TYPE_CHECKING
if TYPE_CHECKING:
    import pandas as pd
    import azureml.dataprep as dprep
    import pyspark.sql


class Resource(yaml.YAMLObject):
    """The base class for resources referenced from briefcase.yaml
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
        child.credentialprovider = self.credentialprovider
            
        return child

    def get_mapped_name(self, name: str):
        """
        Resource secrets name can be remapped using the name: property.
        """
        # check if name: property exists
        # check if name key in property exists
        return self.name[name] if 'name' in self.__dict__ and name in self.name else None

    def init(self, workspace, path, name: str):
        # avoid duplicate initialize
        if '_Resource__workspace' in self.__dict__:
            return

        self.__logger = logging.getLogger('workspace')
        self.__names = set()
        self.__client = None

        self.__workspace = workspace

        # check if we have name mapping
        mapping = self.get_mapped_name('secret')
        if not mapping is None:
            self.__names.add(mapping)

        # TODO: what's the preferred behavior. try as much as possible?
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
        # TODO: filter credentialprovider or change to _?
        return {k: v for k, v in self.__dict__.items()
                if not (k.startswith('_') or k in exclude)}

    def get_credentials_providers(self):
        # TODO: the order of the providers
        # 1. silent ones (e.g. env/keyring/managed service identity? but it takes time to figure?)
        # 2. the specified one (e.g. device login)
        # 3. interactive fallback (e.g. prompt the user)

        # 1. check credentials attribute
        # 1a. find all credential stores (sort alphabetical)
        if 'credentialprovider' in self.__dict__:
            return [self.credentialprovider]
        else:
            from .credentialprovider import CredentialProvider, EnvironmentCredentialProvider, DotEnvCredentialProvider
            from .python.keyring import KeyRingCredentialProvider
            from .python.jupyterlab_credentialprovider import JupyterLabCredentialProvider

            return [
                JupyterLabCredentialProvider(),
                KeyRingCredentialProvider(),
                EnvironmentCredentialProvider(),
                DotEnvCredentialProvider(self.get_workspace().get_env()),
                # include credential providers as well
                *self.get_workspace().get_all_of_type(CredentialProvider)]

    def get_names(self) -> Set[str]:
        return self.__names

    def get_workspace(self) -> 'Briefcase':
        return self.__workspace

    def get_secret(self, **kwargs) -> str:
        return self.__get_secret(self.get_names(), **kwargs)

    def __get_secret(self, names: List[str], **kwargs) -> str:
        # rules to resolve
        # 3. resolve key by name
        # 3a. resolve key by path + name (. seperated) 

        providers = self.get_credentials_providers()    
        try:
            # try all credential provides first
            for provider in providers:
                # make sure we don't use the same provider twice
                if 'get_secret_lock' in provider.__dict__:
                    continue
                provider.get_secret_lock = True
                
                for key in names:
                    self.get_logger().debug("secret probing: {} for {} ...".format(provider.__class__.__name__, key))
                    secret = provider.get_secret(key, **kwargs)
        
                    if secret is not None:
                        self.get_logger().debug("secret found:  {} {}".format(provider.__class__.__name__, key))
                        return secret
        finally:
            for provider in providers:
                provider.__dict__.pop('get_secret_lock', None)

        # contain probed provider names in exception
        provider_names = map(lambda p: p.__class__.__name__, providers)
        raise KeyNotFoundException(
            "Secret not found for keys {} not found in {}".format(names, ", ".join(provider_names)))

    def __getattr__(self, name):
        # print('__getattr__ {}'.format(name))

        # used by pyyaml
        if name == '__setstate__':
            raise AttributeError()

        try:
            mapped = self.get_mapped_name(name)
            if not mapped is None:
                # for the default secret we probe all options. should do the same here?
                value = self.__get_secret([mapped])
            else:
                value = self.__get_secret(list(map(lambda n: '{}.{}'.format(n, name), self.get_names())))

            # cache for next time
            self.__dict__[name] = value

            return value
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

            start_time = timeit.default_timer()

            try:
                # invoke sub-class
                self.__client = self.get_client_lazy()
            except ImportError as error:
                raise Exception("Failed to import {}. Try installing '{}'".format(error, self.pip_package))

            elapsed = timeit.default_timer() - start_time
            self.get_logger().debug("created client ({:.1f} sec): {}".format(elapsed, type(self).__name__))

        return self.__client


class KeyNotFoundException(Exception):
    pass
