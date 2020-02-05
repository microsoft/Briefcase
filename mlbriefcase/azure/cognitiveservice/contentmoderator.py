from ...base import Resource

class contentmoderator(Resource):
    pip_package = 'azure-cognitiveservices-vision-contentmoderator'

    def get_client_lazy(self):
        from azure.cognitiveservices.vision.contentmoderator import ContentModeratorClient
        from msrest.authentication import CognitiveServicesCredentials

        return ContentModeratorClient(self.url, CognitiveServicesCredentials(self.get_secret()))
 