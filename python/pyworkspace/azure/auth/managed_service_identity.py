from ...base import Resource


class ManagedServiceIdentity(Resource):
    yaml_tag = u'!azure.msi'

    def __init__(self):
        pass

    def get_client_lazy(self):
        try:
            from msrestazure.azure_active_directory import MSIAuthentication

            # TODO: add support for other resource types
            msi_auth = MSIAuthentication()
            msi_auth.set_token()

            return msi_auth
        except Exception as e:
            return None
