from ...base import Resource

class textanalytics(Resource):
    pip_package = 'azure-cognitiveservices-language-textanalytics'

    def get_client_lazy(self):
        from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient
        from msrest.authentication import CognitiveServicesCredentials

        return TextAnalyticsClient(self.url, CognitiveServicesCredentials(self.get_secret()))
 