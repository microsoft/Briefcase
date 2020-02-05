from ...base import Resource

class spellcheck(Resource):
    pip_package = 'azure-cognitiveservices-language-spellcheck'

    def get_client_lazy(self):
        from azure.cognitiveservices.language.spellcheck import SpellCheckAPI
        from msrest.authentication import CognitiveServicesCredentials

        return SpellCheckAPI(CognitiveServicesCredentials(self.get_secret()), self.url)
 