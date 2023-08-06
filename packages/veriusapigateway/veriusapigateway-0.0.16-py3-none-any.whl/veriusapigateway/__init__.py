import requests
import json
import re


class VeriUsAPIGateway:

    def __init__(self, username, password=None):
        self.username = username
        self.password = password
        self.headers = {'Content-Type': 'application/json', 'Authorization': "Bearer " + self.username}

    @staticmethod
    def clean_text(text):
        return text.replace('\r', ' ').replace('\b', ' ').replace('\f', ' ').replace('\v', ' ')\
            .replace('\r\n', ' ').replace('"', " ").replace('\t', ' ')\
            .replace('\n', ' ').replace('\'', ' ').replace('\\', ' ').replace('\"', ' ').strip()

    def __post_to_access(self, text1, service_name, text2=None):
        text1 = self.clean_text(text1)
        if not text2:
            data = '{"service_name":"' + service_name + '", "text":"' + text1 + '"}'
        else:
            text2 = self.clean_text(text2)
            data = '{"service_name":"' + service_name + '", "text":"' + text1 + '","text2":"' + text2 + '"}'
        try:
            response = requests.post("http://167.99.142.246:8000/access",
                                     headers=self.headers, data=data.encode('utf-8'))
            response_text = json.loads(response.text)
            return response_text["result"]
        except Exception as e:
            print(e)
            print("Something happened while posting data to webservice:")
            print("Data:", text1)
            if text2:
                print("Data2:", text2)
            return None

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

    def getNormal(self, text):
        return self.__post_to_access(text, "normalization")

    def getDeasciified(self, text):
        return self.__post_to_access(text, "deasciifier")

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

    def getSentenceTokens(self, text):
        return self.__post_to_access(text, "sentencetokenizer")
