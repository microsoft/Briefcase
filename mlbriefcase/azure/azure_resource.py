from ..base import Resource

class AzureResource(Resource):
    def get_subscriptions(self) -> 'List[AzureSubscription]':
        from .subscription import AzureSubscription

        subscriptions = self.get_briefcase().get_all_of_type(AzureSubscription)

        # no subscriptions configured try to auto resolve through MSI
        if len(subscriptions) == 0:
            sub = self.update_child(AzureSubscription())
            
            subscriptions.append(sub)
        
        return subscriptions

    def get_resource_group(self):
        return getattr(self, 'resource_group', None)

    def get_auth_client(self):
        if not hasattr(self, 'auth_client'):
            from .auth.managed_service_identity import ManagedServiceIdentity
            
            # fallback to MSI
            self.get_logger().debug('auth client lookup: defaulting to Microsoft Managed Service Identity')
            self.auth_client = self.get_briefcase().get_global('azure_auth_client', ManagedServiceIdentity)
            
            client = self.auth_client.get_client()
            if client is None:
                # import only when needed
                from .auth.user_with_device_code import AzureUserWithDeviceLogin
                
                self.get_logger().debug('auth client lookup: defaulting to Microsoft User with Device Login')
                
                self.auth_client = self.get_briefcase().get_global('azure_auth_client', AzureUserWithDeviceLogin)
            
        # this can also be a service principal or device auth
        return self.auth_client # .get_client()
