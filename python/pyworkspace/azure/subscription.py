from ..base import Resource
from .azure_resource import AzureResource
from .auth import managed_service_identity
from typing import List


class AzureSubscription(AzureResource):
    yaml_tag = u'!azure.subscription'

    def __init__(self, id=None, ids=[]):
        self.ids = ids

        if id is not None:
            self.ids.append(id)

    def get_resource_group(self):
        return getattr(self, 'resourcegroup', None)

    def get_ids(self) -> List[str]:
        ret = []

        if hasattr(self, 'id'):
            ret.append(self.id)

        if hasattr(self, 'ids'):
            ret.extend(self.ids)

        if len(ret) == 0:
            # TODO: resolve configured msi
            auth = self.get_auth_client()
            if auth is not None:
                try:
                    # let's try to enumerate subscriptions
                    from azure.mgmt.subscription import SubscriptionClient
                    subscription_client = SubscriptionClient(auth)

                    ret.extend(map(lambda s: s.subscription_id,
                                   subscription_client.subscriptions.list()))
                except:
                    pass

        return ret
