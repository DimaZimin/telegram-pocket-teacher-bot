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
        definitions = ''
        for entry in self.data['entries']:
            for lexeme in entry['lexemes']:
                for definition in lexeme['senses']:
                     definitions = definitions + f'\n({lexeme["partOfSpeech"]}) \t {definition["definition"]}\n'
        if definitions:
            return definitions
        else:
            return "Sorry, I can't find that word"

    def audio(self):
        audio_urls = []
        try:
            for entry in self.data['entries']:
                for pronunciation in entry['pronunciations']:
                    audio_urls.append(pronunciation['audio']['url'])
        except KeyError:
            print('')
        return audio_urls
