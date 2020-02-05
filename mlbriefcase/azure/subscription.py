from ..base import Resource
from .azure_resource import AzureResource
from .auth import managed_service_identity
from typing import List


class subscription(AzureResource):
    pip_package = 'azure-mgmt-subscription'

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
                self.get_logger().debug('auth client found: {}. auto-discovering Azure subscriptions'.format(auth.__class__.__name__))
                try:
                    # let's try to enumerate subscriptions
                    from azure.mgmt.subscription import SubscriptionClient
                    subscription_client = SubscriptionClient(auth.get_client())

                    ret.extend(map(lambda s: s.subscription_id,
                                   subscription_client.subscriptions.list()))
                except Exception as e:
                    self.get_logger().debug('unable to auto-resolve Azure subscriptions as no auth_client found {}'.format(e))
                    pass
            else:
                self.get_logger().debug('unable to auto-resolve Azure subscriptions as no auth_client found')

        return ret
