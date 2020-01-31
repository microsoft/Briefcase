from ...base import Resource

class vision(Resource):
    pip_package = 'azure-cognitiveservices-vision-computervision'

    def get_client(self):
        from azure.cognitiveservices.vision.computervision import ComputerVisionClient
        from msrest.authentication import CognitiveServicesCredentials

        return ComputerVisionClient(self.url, CognitiveServicesCredentials(self.get_secret()))
 