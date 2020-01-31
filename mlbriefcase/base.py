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

class Resource:
    """The base class for resources referenced from briefcase.yaml
    """
    
    def get_logger(self):
        return self.__logger

    def update_child(self, child):
        child.name = self.name
        child.init(self.__briefcase, dict())
        # TODO: should child created resource inherit the credential provider?
        # child.credentialprovider = self.credentialprovider
            
    #     return child

    # def get_mapped_name(self, name: str):
    #     """
    #     Resource secrets name can be remapped using the name: property.
    #     """
    #     # check if name: property exists
    #     # check if name key in property exists
    #     return self.name[name] if 'name' in self.__dict__ and name in self.name else None

    def init(self, briefcase, mappings):
        self.__logger = logging.getLogger('briefcase')
        self.__client = None
        self.__briefcase = briefcase
        self.__mappings = mappings

    def get_credentials_providers(self):
        # TODO: the order of the providers
        # 1. silent ones (e.g. env/keyring/managed service identity? but it takes time to figure?)
        # 2. the specified one (e.g. device login)
        # 3. interactive fallback (e.g. prompt the user)

        # 1. check credentials attribute
        # 1a. find all credential stores (sort alphabetical)
        if 'credentialprovider' in self.__dict__:
            return [self.get_briefcase()[self.credentialprovider]]
        else:
            from .credentialprovider import CredentialProvider, EnvironmentCredentialProvider, DotEnvCredentialProvider
            from .python.keyring import keyring
            from .python.jupyterlab_credentialprovider import jupyterlabCredentialProvider

            return [
                jupyterlabCredentialProvider(),
                keyring(),
                EnvironmentCredentialProvider(),
                DotEnvCredentialProvider(self.get_briefcase().get_env()),
                # include credential providers as well
                *self.get_briefcase().get_all_of_type(CredentialProvider)]

    def get_briefcase(self) -> 'Briefcase':
        return self.__briefcase

    def get_secret(self, **kwargs) -> str:
        # allow remapping of the secret
        name = self.name
        if 'secret' in self.__mappings:
            name = self.__mappings['secret']

        return self.__get_secret(name, **kwargs)

    def __get_secret(self, name: str, **kwargs) -> str:
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
                
                self.get_logger().debug("secret probing: {} for {} ...".format(provider.__class__.__name__, name))
                secret = provider.get_secret(name, **kwargs)
        
                if secret is not None:
                    self.get_logger().debug("secret found:  {} {}".format(provider.__class__.__name__, name))
                    return secret
        finally:
            for provider in providers:
                provider.__dict__.pop('get_secret_lock', None)

        # contain probed provider names in exception
        provider_names = map(lambda p: p.__class__.__name__, providers)
        raise KeyNotFoundException(
            "Secret not found for keys {} not found in {}".format(name, ", ".join(provider_names)))

    def __getattr__(self, name):
        # check if a re-mapping exists
        if name in self.__mappings:
            property_name = self.__mappings[name]
        else:
            property_name = '{}.{}'.format(self.name, name)

        try:
            value = self.__get_secret(property_name)

            # cache for next time
            self.__dict__[name] = value

            return value
        except KeyNotFoundException:
            raise AttributeError("Attribute '{}' ({}) not found".format(name, property_name))

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
