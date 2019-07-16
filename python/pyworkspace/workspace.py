import yaml
import os
from typing import Any, Callable, List, Union, Type
import re

from .azure import *
from .azure.cognitiveservice import *
from .base import *
from .datasource import *
from .credentialprovider import *

class Workspace:
    def __init__(self, path: str=None, content: str=None):
        # handle various defaults
        if content is None:
            if path is None:
                # TODO: do we need to pass the search directory?
                path = self.__find_yaml('.')
            
            with open(path, 'r') as f:
                content = f.read()

        self.__parse(content)

    def __find_yaml(self, path):   
        path = os.path.realpath(path)

        for name in os.listdir(path):
            # TODO: allow for different name. global param? ctor param?
            if name == 'resources.yaml' or name == 'resources.yml':
                return os.path.join(path, name)

        new_path = os.path.realpath(os.path.join(path, '..'))
        if path == new_path:
            raise Exception("Unable to find resources.yaml")

        return self.__find_yaml(new_path)

    def __parse(self, content: str):
        # don't fail for future types
        # TODO: don't set this up globally
        # loader = yaml.Loader()
        yaml.add_multi_constructor('!', lambda loader, suffix, node: None)

        self.resources = yaml.load(content)

        # visit all nodes and setup links
        def setup_links(n, path, name):
            n.__workspace = self
            n.__path = path
            n.__name = name        

        self.visit(setup_links)

    # setup root links to avoid back reference to credential provider
    def visit(self,
              action: Callable[[yaml.YAMLObject, List[str], str], Any],
              path: List[str] = [],
              node: Any = None) -> List:
        if node is None:
            node = self.resources

        ret = []
        for k, n in node.items():
            if isinstance(n, dict):
                ret.extend(self.visit(action, [*path, k], n))
            elif isinstance(n, yaml.YAMLObject):
                v = action(n, path, k) 
                if v is not None:
                    ret.append(v)

        return ret

    def get_all_of_type(self, type: Type):
        return self.visit(lambda node, _, __: node if isinstance(node, type) else None)

    key_split_regex = re.compile('[./]')

    def __getitem__(self, key: str) -> Union[Resource, List[Resource]]:
        path = Workspace.key_split_regex.split(key)

        if len(path) == 1:
            # search all
            ret = self.visit(lambda node, _, name: node if name == key else None)
            ret_len = len(ret)

            # make it convenient
            if ret_len == 0:
                return None
            elif ret_len == 1:
                return ret[0]
            else:
                ret
        else:
            # if it's a path find the precise one
            node = self.resources
            for name in path:
                node = node[name]
            return node