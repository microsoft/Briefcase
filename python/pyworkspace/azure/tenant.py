from ..base import Resource
from .azure_resource import AzureResource
from .auth import managed_service_identity
from typing import List


class AzureTenant(AzureResource):
    yaml_tag = u'!azure.tenant'

    def __init__(self, id=None):
        self.id = id