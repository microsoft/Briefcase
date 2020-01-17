from ...base import Resource

class AzureCognitiveServiceFace(Resource):
    yaml_tag = u'!azure.cognitiveservice.face'
    pip_package = 'azure-cognitiveservices-vision-face'
    
    def __init__(self, url):
        self.url = url

    def get_client_lazy(self, **kwargs):
        from azure.cognitiveservices.vision.face import FaceClient
        from msrest.authentication import CognitiveServicesCredentials

        return FaceClient(self.url, CognitiveServicesCredentials(self.get_secret()))