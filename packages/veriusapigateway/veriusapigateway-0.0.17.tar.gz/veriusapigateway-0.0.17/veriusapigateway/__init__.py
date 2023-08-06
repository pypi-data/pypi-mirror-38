import requests
import json
from configs.configurations import Configurations


class VeriUsAPIGateway:

    def __init__(self, username, password=None):
        self.username = username
        self.password = password
        self.headers = {'Content-Type': 'application/json', "apikey": self.username}
        self.cfg = Configurations()

    @staticmethod
    def clean_text(text):
        return text.replace('\r', ' ').replace('\b', ' ').replace('\f', ' ').replace('\v', ' ')\
            .replace('\r\n', ' ').replace('"', " ").replace('\t', ' ')\
            .replace('\n', ' ').replace('\'', ' ').replace('\\', ' ').replace('\"', ' ').strip()

    def __post_to_access(self, endpoint, text1, text2=None):
        text1 = self.clean_text(text1)
        if not text2:
            data = '{"text":"' + text1 + '"}'
        else:
            text2 = self.clean_text(text2)
            data = '{"text1":"' + text1 + '","text2":"' + text2 + '"}'
        try:
            response = requests.post(self.cfg.gateway_url + endpoint,
                                     headers=self.headers, data=data.encode('utf-8'))
            response_text = json.loads(response.text)
            result = response_text["result"]
        except:
            print(response)
            result = response.text["message"]
            print(result)
        return result

    def getTextSimilarity(self, text1, text2):
        return self.__post_to_access(text1, "textsimilarity", text2)

    def getSemanticSimilarity(self, text1, text2):
        return self.__post_to_access(text1, "semanticsimilarity", text2)

    def getLanguage(self, text):
        return self.__post_to_access(text, "languagedetection")

    def getPartofSpeechTags(self, text):
        return self.__post_to_access(text, "postagger")

    def getAbusive(self, text):
        return self.__post_to_access(text, "abusivecontentdetection")

    def getSummary(self, text):
        return self.__post_to_access(text, "textsummarization")

    def getKeywords(self, text):
        return self.__post_to_access(text, "keywordextraction")

    def getNamedEntities(self, text):
        return self.__post_to_access(text, "entityextraction")

    def getDistorted(self, text):
        return self.__post_to_access(text, "distortedlanguagedetection")

    def getIntent(self, text):
        return self.__post_to_access(text, "intentdetection")

    def getNewsClass(self, text):
        return self.__post_to_access(text, "newsclassification")


    def getProductCategory(self, text):
        return self.__post_to_access(text, "productcategoryclassification")

    def getMorphology(self, text):
        text = self.clean_text(text)
        data = '{"data":"' + text + '"}'
        headers = {'Content-Type': 'application/json', }
        response = requests.post('http://167.99.142.246:8019/morphology', headers=headers,
                                 data=data.encode('utf-8'), auth=(self.username, self.password))
        return json.loads(response.text)['data']

    def getSexual(self, text):
        return self.__post_to_access(text, "sexualcontentdetection")

    def getGibberish(self, text):
        return self.__post_to_access(text, "gibberishdetection")

    ######

    def get_normal(self, text):
        return self.__post_to_access(endpoint=self.cfg.normalization_endpoint, text1=text)

    def get_deasciified(self, text):
        return self.__post_to_access(endpoint=self.cfg.deasciifier_endpoint, text1=text)

    def get_sentence_tokens(self, text):
        return self.__post_to_access(endpoint=self.cfg.sentence_tokenizer_endpoint, text1=text)

    def get_sentiment(self, text):
        return self.__post_to_access(endpoint=self.cfg.sentiment_analysis_endpoint, text1=text)
