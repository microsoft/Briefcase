import os
from typing import Any, Callable, List, Union, Type
import re
import yaml
import logging
import importlib
import json
import jsonschema
from importlib_resources import read_text

from .azure import *
from .amazon import *
from .google import *
from .clarifai import *
from .base import *
from .datasource import *
from .credentialprovider import *
from .python import *
from dotenv import dotenv_values

"""A Briefcase instance parsing a briefcase.yaml and exposing the resources.
"""
class Briefcase:
    def __init__(self, path: str = None, content: str = None):
        """Initializes a briefcases
        
        Keyword Arguments:
            path {str} -- optional path to YAML. If not supplied searches the current directory and recurses up. (default: {None})
            content {str} -- optional content to the YAML. (default: {None})
        """
        self.logger = logging.getLogger('briefcase')
        # TODO: think about multiple yamls and when to actually stop
        # force user to supply path
        # stop at .git directory (what about .svn?)

        # handle various defaults
        if content is None:
            if path is None:
                path = self.__find_yaml('.')

            self.logger.debug('briefcase: {}'.format(path))
            with open(path, 'r') as f:
                content = f.read()

        self.__parse(content)
        self.globals = {}

        # load the .env next to the found .yaml
        dot_env_path = os.path.join(os.path.dirname(os.path.abspath(path)), '.env')
        self.logger.debug('.env: {}'.format(dot_env_path))
        self.__env = dotenv_values(dot_env_path)

    def get_env(self) -> Dict[str, str]:
        return self.__env

    def __find_yaml(self, path) -> str:
        path = os.path.realpath(path)

        for name in os.listdir(path):
            # TODO: allow for different name. global param? ctor param?
            if name == 'briefcase.yaml':
                return os.path.join(path, name)

        # going up the directory structure
        new_path = os.path.realpath(os.path.join(path, '..'))
        if path == new_path:  # hit the root
            raise Exception("Unable to find briefcase.yaml")

        return self.__find_yaml(new_path)

    def __validate(self, yaml_resources):
        # validate yaml
        schema = read_text('mlbriefcase', 'briefcase-schema.json')
        jsonschema.validate(yaml_resources, json.loads(schema))

    def __parse(self, content: str):
        # load the yaml file
        yaml_resources = yaml.safe_load(content)

        # support empty file
        if yaml_resources is None:
            self.resource_lookup = {}
            self.resources = []
            return

        # validete against JSON schema
        self.__validate(yaml_resources)

        def visit_new(node: Any, path: List[str]) -> List:
            # resources have names
            if 'name' in node:
                module = importlib.import_module("." + ".".join(path[:-1]), "mlbriefcase")
                class_ = getattr(module, path[-1])
    
                # create resource
                resource = class_()

                # copy data
                mappings = dict()
                for k, v in node.items():
                    if isinstance(v, str) or k == 'metadata':
                        setattr(resource, k, v)
                        continue

                    # else it must be a mapping
                    mappings[k] = v['key']

                resource.init(self, mappings)

                return [resource]

            ret = []
            if (type(node) == list):
                for n in node:
                    ret.extend(visit_new(n, path))
            elif (type(node) == dict):
                for k, n in node.items():
                    ret.extend(visit_new(n, [*path, k]))
            else:
                raise Exception("node type {} not supported".format(type(node)))

            return ret

        self.resources = visit_new(yaml_resources, [])
        self.resource_lookup = dict(map(lambda r: [r.name, r], self.resources))

    def get_all_of_type(self, type: Type):
        return list(filter(lambda resource: isinstance(resource, type), self.resources))

    def get_all(self):
        return self.resources

    key_split_regex = re.compile('[./]')

    def get_global(self, key: str, type: Type):
        # combine key with type to make it unique
        key = '{}.{}'.format(key, type.__name__)
        
        if not(key in self.globals):
            self.logger.debug('registering global: {}'.format(key))
            
            resource = type()
            resource.add_name(self, [], key)
            
            self.globals[key] = resource
        
        return self.globals[key]
    
    def __getitem__(self, key: str) -> Resource:
        if key in self.resource_lookup:
            return self.resource_lookup[key]
        
        return None