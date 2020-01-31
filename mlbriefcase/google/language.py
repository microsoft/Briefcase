from .google_base import *

class language(GoogleBase):
	"""
	Google NER Service <https://cloud.google.com/natural-language/docs/analyzing-entities>'
	"""

	pip_package = 'google-cloud-language'
	
	def get_client_lazy(self, **kwargs):
		from google.cloud import language
		return language.LanguageServiceClient(credentials=self.get_credential())
