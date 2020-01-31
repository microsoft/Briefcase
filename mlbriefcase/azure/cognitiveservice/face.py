from ...base import Resource

class face(Resource):
    pip_package = 'azure-cognitiveservices-vision-face'
    
    def get_client_lazy(self, **kwargs):
        from azure.cognitiveservices.vision.face import FaceClient
        from msrest.authentication import CognitiveServicesCredentials

        return FaceClient(self.url, CognitiveServicesCredentials(self.get_secret()))