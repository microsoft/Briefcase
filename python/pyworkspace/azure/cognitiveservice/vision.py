from ...base import Resource

class AzureCognitiveServiceVision(Resource):
    yaml_tag = u'!azure.cognitiveservice.vision'
    pip_package = 'azure-cognitiveservices-vision-computervision'

    # defaults
    # https://www.terraform.io/docs/providers/azurerm/r/cognitive_account.html
    # translate https://www.terraform.io/docs/configuration/functions/yamldecode.html   
    # terraform = { 
        # name -> get_name()
        # 'type': 'azurerm_cognitive_account',
        # 'kind': 'Face',
        # 'sku': 'S0',
        # 'tier': 'Free',
        # location
        # resource_group
    # }

    def __init__(self, url):
        self.url = url

    def get_client(self):
        from azure.cognitiveservices.vision.computervision import ComputerVisionClient
        from msrest.authentication import CognitiveServicesCredentials

        return ComputerVisionClient(self.url, CognitiveServicesCredentials(self.get_secret()))
 