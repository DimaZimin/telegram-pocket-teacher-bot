import requests
import json

with open('token.json') as json_file:
    token = json.load(json_file)


class Dictionary:

    source = "https://lingua-robot.p.rapidapi.com/language/v1/entries/en/"

    headers = {
        'x-rapidapi-host': "lingua-robot.p.rapidapi.com",
        'x-rapidapi-key': token['API_KEY_DICTIONARY']
    }

    def __init__(self, word):

        self.url = self.source + word

        self.response = requests.request("GET", self.url, headers=self.headers)

        self.data = self.response.json()

    def definitions(self):
        definitions = []
        for entry in self.data['entries']:
            for lexeme in entry['lexemes']:
                for definition in lexeme['senses']:
                    definitions.append((lexeme['partOfSpeech'],definition['definition']))
        return definitions

    def audio(self):
        audio_urls = []
        for entry in self.data['entries']:
            for pronunciation in entry['pronunciations']:
                try:
                    audio_urls.append(pronunciation['audio']['url'])
                except KeyError:
                    print('')
        return audio_urls



class GoogleDictAPI:

    source = 'https://api.dictionaryapi.dev/api/v1/entries/en/'

    def __init__(self, word):

        self.url = self.source + word

        self.response = requests.request("GET", self.url)

        self.data = self.response.json()

    def word_origin(self):
        for word in self.data:
            return word['origin']

    def synonim(self):
        synonyms = ''
        for word in self.data:
            for meaning in word:
                return

di = GoogleDictAPI('fly')

print(di.word_origin())