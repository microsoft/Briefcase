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
                self.logger.debug('auth client found: {}. auto-discovering Azure subscriptions'.format(auth.__class__.__name__))
                try:
                    # let's try to enumerate subscriptions
                    from azure.mgmt.subscription import SubscriptionClient
                    subscription_client = SubscriptionClient(auth.get_client())

                    ret.extend(map(lambda s: s.subscription_id,
                                   subscription_client.subscriptions.list()))
                except Exception as e:
                    self.logger.debug('unable to auto-resolve Azure subscriptions as no auth_client found {}'.format(e))
                    pass
            else:
                self.logger.debug('unable to auto-resolve Azure subscriptions as no auth_client found')

        return ret
