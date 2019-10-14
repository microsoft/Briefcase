from ...base import Resource

class AzureCognitiveServiceFace(Resource):
    yaml_tag = u'!azure.cognitiveservice.face'
    def __init__(self, url):
        self.url = url

    def get_client(self):
        try:
            from azure.cognitiveservices.vision.face import FaceClient
            from msrest.authentication import CognitiveServicesCredentials

            return FaceClient(self.url, CognitiveServicesCredentials(self.get_secret()))
        except:
            print ("Error missing package: run 'pip install --upgrade azure-cognitiveservices-vision-face'")
            pass 
 