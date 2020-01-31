from .aws_boto3 import *

class comprehend(AwsBoto3):
	"""
	Amazon's Comprehend Service <https://docs.aws.amazon.com/comprehend/latest/dg/get-started-api-sentiment.html>
	"""

	def get_client_lazy(self, **kwargs):
	 return super().get_client_lazy('comprehend', region_name=self.region_name, **kwargs)

	# TODO: one could add a shared signature spanning Azure, AWS, GCP,... 