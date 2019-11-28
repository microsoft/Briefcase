from .aws_boto3 import *
from .rekognition import *
from .comprehend import *
from .s3 import *

from .aws_boto3 import *

class AwsS3(AwsBoto3):
	"""
	Amazon's S3 Service <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html>
	"""

	yaml_tag = u'!aws.s3'
	
	def get_client_lazy(self, **kwargs):
		return super().get_client_lazy('s3')

	# def get_url(self) -> str:
		# return self.get_client().generate_presigned_url()
