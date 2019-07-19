from ...base import Resource

class AzureServicePrincipal(Resource):
    yaml_tag = u'!azure.serviceprincipal'
    
    def __init__(self, clientid, tenantid):
        self.clientid = clientid
        self.tenantid = tenantid

    def get_client(self):
        from azure.common.credentials import ServicePrincipalCredentials

        # TODO add cloud environment
        return ServicePrincipalCredentials(client_id=self.clientid,
                                           secret=self.get_secret(),
                                           tenant=self.tenantid)
