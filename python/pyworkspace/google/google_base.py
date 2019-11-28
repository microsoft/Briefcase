from ..base import Resource
import json

class GoogleBase(Resource):
	def get_credential(self):
		from google.oauth2.service_account import Credentials

		return Credentials.from_service_account_info(json.loads(self.get_secret()))
