from ..base import Resource

class ClarifaiApp(Resource):
	"""
	Clarifai Moderation image SDK <https://docs.clarifai.com/api-guide/predict>
	"""

	yaml_tag = u'!clarifai.app'
	pip_package = 'clarifai'

	def get_client_lazy(self, **kwargs):
		from clarifai.rest import ClarifaiApp

		return ClarifaiApp(api_key=self.get_secret())