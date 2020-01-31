from ...base import Resource

class managedserviceidentity(Resource):
    def get_client_lazy(self):
        return self.get_client_for_resource()
        
    def get_client_for_resource(self, resource='https://management.core.windows.net/'):
        # TODO: cache client
        try:
            from msrestazure.azure_active_directory import MSIAuthentication

            msi_auth = MSIAuthentication(resource)
            msi_auth.set_token()

            return msi_auth
        except Exception as e:
            # TODO: module exception pip install --upgrade msrestazure
            return None
        
