from ...base import Resource

class AzureCognitiveServiceAnomalyDetection(Resource):
    yaml_tag = u'!azure.cognitiveservice.anomalydetection'
    def __init__(self, url):
        self.url = url

    def get_client(self):
        try:
            from azure.cognitiveservices.anomalydetector import AnomalyDetectorClient
            from msrest.authentication import CognitiveServicesCredentials

            return AnomalyDetectorClient(self.url, CognitiveServicesCredentials(self.get_secret()))
        except:
            print ("Error missing package: run 'pip install --upgrade azure-cognitiveservices-anomalydetector'")
            pass 
 