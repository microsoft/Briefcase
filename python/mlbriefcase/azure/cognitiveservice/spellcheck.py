from ...base import Resource

class AzureCognitiveServiceSpellCheck(Resource):
    yaml_tag = u'!azure.cognitiveservice.spellcheck'
    def __init__(self, url):
        self.url = url

    def get_client(self):
        try:
            from azure.cognitiveservices.language.spellcheck import SpellCheckAPI
            from msrest.authentication import CognitiveServicesCredentials

            return SpellCheckAPI(CognitiveServicesCredentials(self.get_secret()), self.url)
        except:
            print ("Error missing package: run 'pip install --upgrade azure-cognitiveservices-language-spellcheck'")
            pass 
 