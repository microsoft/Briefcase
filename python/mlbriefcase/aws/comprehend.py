from .aws_boto3 import *

class AwsComprehend(AwsBoto3):
	"""
	Amazon's Comprehend Service <https://docs.aws.amazon.com/comprehend/latest/dg/get-started-api-sentiment.html>
	"""

	yaml_tag = u'!aws.comprehend'
	
	def get_client_lazy(self, **kwargs):
	 return super().get_client_lazy('comprehend', region_name=self.region_name, **kwargs)

	# TODO: one could add a shared signature spanning Azure, AWS, GCP,... 