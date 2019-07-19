from ...base import Resource

class AzureUserWithDeviceLogin(Resource):
    yaml_tag = u'!azure.userwithdevicelogin'
    
    def __init__(self, clientid, tenantid):
        self.clientid = clientid
        self.tenantid = tenantid

    def get_client(self):
        import adal

        # https://github.com/Azure-Samples/key-vault-python-authentication/blob/master/authentication_sample.py
        # create an adal authentication context
        auth_context = adal.AuthenticationContext('https://login.microsoftonline.com/%s' % self.tenantid)

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
                token = auth_context.acquire_token_with_device_code(resource=resource,
                                                                    client_id=xplat_client_id,
                                                                    user_code_info=user_code_info)

            token_state[0] = token
            # TODO: refresh? see token_state['expiresOn']
            return token['tokenType'], token['accessToken']

        return adal_callback

