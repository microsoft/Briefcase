from ...base import Resource

class serviceprincipal(Resource):
    def get_client_lazy(self):
        from azure.common.credentials import ServicePrincipalCredentials

        # TODO add cloud environment
        return ServicePrincipalCredentials(client_id=self.clientid,
                                           secret=self.get_secret(),
                                           tenant=self.tenantid)

        # TODO: pip install
