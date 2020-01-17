from ..base import Resource

class AwsBoto3(Resource):
	pip_package = 'boto3'

	def get_client_lazy(self, name, **kwargs):
		import boto3
		
		return boto3.client(
			name, 
			aws_access_key_id=self.key_id,
			aws_secret_access_key=self.get_secret(),
			 **kwargs)