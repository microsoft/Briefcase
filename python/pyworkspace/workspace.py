import os
from typing import Any, Callable, List, Union, Type
import re
import yaml
import logging

# TODO: check if the imports are needed
from .azure import *
from .base import *
from .datasource import *
from .credentialprovider import *
from .python import *
from dotenv import dotenv_values

class Workspace:
    def __init__(self, path: str = None, content: str = None):
        self.logger = logging.getLogger('workspace')
        # TODO: think about multiple yamls and when to actually stop
        # force user to supply path
        # stop at .git directory (what about .svn?)

        # handle various defaults
        if content is None:
            if path is None:
                path = self.__find_yaml('.')

            self.logger.debug('workspace: {}'.format(path))
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
            if name == 'resources.yaml':
                return os.path.join(path, name)

        # going up the directory structure
        new_path = os.path.realpath(os.path.join(path, '..'))
        if path == new_path:  # hit the root
            raise Exception("Unable to find resources.yaml")

        return self.__find_yaml(new_path)

    def __parse(self, content: str):
        # TODO: don't fail for future types. the safe_load thing is the right approach, but
        #       this will lead to failures ones new types are introduced and the workspace library
        #       is still old...

        # Still loading using SafeLoader, but making sure unknown tags are ignored
        # https://security.openstack.org/guidelines/dg_avoid-dangerous-input-parsing-libraries.html
        # self.resources = yaml.safe_load(content)

        class SafeLoaderIgnoreUnknown(yaml.SafeLoader):
            def ignore_unknown(self, node):

                return None

        SafeLoaderIgnoreUnknown.add_constructor(
            None, SafeLoaderIgnoreUnknown.ignore_unknown)
        self.resources = yaml.load(content, Loader=SafeLoaderIgnoreUnknown)

        # visit all nodes and setup links
        def setup_links(node, path, name):
            # make sure we don't overwrite path/name from a reference usage (e.g. *foo)
            # &foo needs to come before *foo
            node.init(self, path, name)

        # setup root links to avoid back reference to credential provider
        self.visit(setup_links)

    def visit_resource(self,
                       action: Callable[[yaml.YAMLObject, List[str], str], Any],
                       path: List[str],
                       node: Any,
                       name: str) -> List:

        ret = []

        # execute action for the reousrce
        v = action(node, path, name)
        if v is not None:
            ret.append(v)

        # recurse into yaml objects to support nested data defs
        for k, n in node.__dict__.items():
            if isinstance(n, yaml.YAMLObject):
                ret.extend(self.visit_resource(
                    action, [*path, name], node=n, name=k))

        return ret

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
                ret.extend(self.visit_resource(action, path, node=n, name=k))

        return ret

    def get_all_of_type(self, type: Type):
        return self.visit(lambda node, _, __: node if isinstance(node, type) else None)

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
    
    def __getitem__(self, key: str) -> Union[Resource, List[Resource]]:
        path = Workspace.key_split_regex.split(key)

        if len(path) == 1:
            # search all
            ret = self.visit(
                lambda node, _, name: node if name == key else None)
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
