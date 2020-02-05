from ...base import Resource

class anomalydetection(Resource):
    pip_package = 'azure-cognitiveservices-anomalydetector'

    def get_client_lazy(self):
        from azure.cognitiveservices.anomalydetector import AnomalyDetectorClient
        from msrest.authentication import CognitiveServicesCredentials

        return AnomalyDetectorClient(self.url, CognitiveServicesCredentials(self.get_secret()))
	