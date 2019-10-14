from ...base import Resource

class AzureCognitiveServiceContentModerator(Resource):
    yaml_tag = u'!azure.cognitiveservice.contentmoderator'
    def __init__(self, url):
        self.url = url

    def get_client(self):
        try:
            from azure.cognitiveservices.vision.contentmoderator import ContentModeratorClient
            from msrest.authentication import CognitiveServicesCredentials

            return ContentModeratorClient(self.url, CognitiveServicesCredentials(self.get_secret()))
        except:
            print ("Error missing package: run 'pip install --upgrade azure-cognitiveservices-vision-contentmoderator'")
            pass 
 