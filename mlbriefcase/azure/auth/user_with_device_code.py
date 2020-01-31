from ...base import Resource
from ..tenant import AzureTenant

class devicecode(Resource):
    def get_tenantid(self):
        if not hasattr(self, 'tenantid'):
            tenants = self.get_briefcase().get_all_of_type(AzureTenant)
            if len(tenants) > 0:
                self.tenantid = tenants[0].id
                self.get_logger().debug('device login: found Azure tenant {}'.format(self.tenantid))
            
        return self.tenantid
        
    def get_client_for_keyvault(self):
        import adal
        from msrestazure.azure_active_directory import AADTokenCredentials

        # https://github.com/Azure-Samples/key-vault-python-authentication/blob/master/authentication_sample.py
        # create an adal authentication context
        auth_context = adal.AuthenticationContext('https://login.microsoftonline.com/%s' % self.get_tenantid())

        # using the XPlat command line client id as it is available across all tenants and subscriptions
        # this would be replaced by your app id
        xplat_client_id = '04b07795-8ddb-461a-bbee-02f9e1bf7b46'
        
        # create a callback to supply the token type and access token on request
        token_state = [None]

        def adal_callback(server, resource, scope, bearer, token_state=token_state):
            token = token_state[0]
            if token is None:
                user_code_info = auth_context.acquire_user_code(resource,
                                                                xplat_client_id)

                print(user_code_info['message'])
                try:
                    import webbrowser
                    webbrowser.open('https://microsoft.com/devicelogin?input='+ user_code_info['user_code'], new=2)
                except:
                    print("Unexpected error:", sys.exc_info()[0])
                    pass
                
                token = auth_context.acquire_token_with_device_code(resource=resource,
                                                                    client_id=xplat_client_id,
                                                                    user_code_info=user_code_info)

            token_state[0] = token
            # TODO: refresh? see token_state['expiresOn']
            return token['tokenType'], token['accessToken']

        return adal_callback
    
    def get_client_lazy(self):
        return self.get_client_for_resource()
    
    def get_client_for_resource(self, resource='https://management.core.windows.net/'):
        import adal
        from msrestazure.azure_active_directory import AADTokenCredentials

        # https://github.com/Azure-Samples/key-vault-python-authentication/blob/master/authentication_sample.py
        # create an adal authentication context
        auth_context = adal.AuthenticationContext('https://login.microsoftonline.com/%s' % self.get_tenantid())

        # using the XPlat command line client id as it is available across all tenants and subscriptions
        # this would be replaced by your app id
        xplat_client_id = '04b07795-8ddb-461a-bbee-02f9e1bf7b46'

        user_code_info = auth_context.acquire_user_code(resource, xplat_client_id)

        print(user_code_info['message'])
        #try:
        #    import webbrowser
        #     webbrowser.open_new('https://microsoft.com/devicelogin?input='+ user_code_info['user_code'])
        # except:
        #    pass
        
        token = auth_context.acquire_token_with_device_code(resource=resource,
            client_id=xplat_client_id,
            user_code_info=user_code_info)
        
        return AADTokenCredentials(token, xplat_client_id)

