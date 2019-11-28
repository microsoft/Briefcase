from .google_base import *

class GoogleVideo(GoogleBase):
	"""
	Google video intelligence for content moderation annotation <https://cloud.google.com/video-intelligence/docs/libraries#client-libraries-install-python>
	"""

	yaml_tag = u'!google.video'
	pip_package = 'google-cloud-video'

	def get_client_lazy(self, **kwargs):
		from google.cloud import videointelligence
		return videointelligence.VideoIntelligenceServiceClient(credentials=self.get_credential())