from ...base import Resource

class AzureCognitiveServiceTextAnalytics(Resource):
    yaml_tag = u'!azure.cognitiveservice.textanalytics'
    def __init__(self, url):
        self.url = url

    def get_client(self):
        try:
            from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient
            from msrest.authentication import CognitiveServicesCredentials

            return TextAnalyticsClient(self.url, CognitiveServicesCredentials(self.get_secret()))
        except:
            print ("Error missing package: run 'pip install --upgrade azure-cognitiveservices-language-textanalytics'")
            pass 
 