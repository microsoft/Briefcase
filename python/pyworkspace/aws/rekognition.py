from .aws_boto3 import *

class AwsRekognition(AwsBoto3):
	yaml_tag = u'!aws.rekognition'

	def get_client_lazy(self, **kwargs):
	 return super().get_client_lazy('rekognition', region_name=self.region_name, **kwargs)