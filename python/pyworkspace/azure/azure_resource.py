from ..base import Resource
from .auth.managed_service_identity import ManagedServiceIdentity


class AzureResource(Resource):
    def get_subscriptions(self) -> 'List[AzureSubscription]':
        from .subscription import AzureSubscription

        subscriptions = self.get_workspace().get_all_of_type(AzureSubscription)

        # no subscriptions configured try to auto resolve through MSI
        if len(subscriptions) == 0:
            subscriptions.append(AzureSubscription())

        return subscriptions

    def get_resource_group(self):
        return getattr(self, 'resource_group', None)

    def get_auth_client(self):
        if not hasattr(self, 'auth_client'):
                # fallback to MSI
            self.auth_client = ManagedServiceIdentity()

            # this can also be a service principal or device auth
        return self.auth_client.get_client()
