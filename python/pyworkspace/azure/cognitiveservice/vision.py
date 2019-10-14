from ...base import Resource

class AzureCognitiveServiceVision(Resource):
    yaml_tag = u'!azure.cognitiveservice.vision'
    def __init__(self, url):
        self.url = url

    def get_client(self):
        try:
            from azure.cognitiveservices.vision.computervision import ComputerVisionClient
            from msrest.authentication import CognitiveServicesCredentials

            return ComputerVisionClient(self.url, CognitiveServicesCredentials(self.get_secret()))
        except:
            print ("Error missing package: run 'pip install --upgrade azure-cognitiveservices-vision-computervision'")
            pass 
 