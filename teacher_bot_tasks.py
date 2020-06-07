from bs4 import BeautifulSoup
import requests



headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:76.0) Gecko/20100101 Firefox/76.0'}



class RandomIdiom:

    url = 'https://randomword.com/idiom'

    source = requests.get(url).text

    soup = BeautifulSoup(source, 'html5lib')

    idiom = soup.find('div', {'id': 'random_word'}).text

    meaning = soup.find('div', {'id': 'random_word_definition'}).text

    @classmethod
    def print_idiom(cls):

        return f'Phrase: {cls.idiom}\nMeaning: {cls.meaning}'


class RandomArtPiece:

    url = 'https://random-ize.com/random-art-gallery/'

    source = requests.get(url,  headers=headers).text

    soup = BeautifulSoup(source, 'html5lib')

    picture_link = 'https://random-ize.com' + soup.find('img')['src']

    picture_name = soup.find('img')['alt']

    description = soup.find_all('center')[1].div.text


def get_idiom():
    url = 'https://randomword.com/idiom'
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'html5lib')
    idiom = soup.find('div', {'id': 'random_word'}).text
    meaning = soup.find('div', {'id': 'random_word_definition'}).text
    return f'Phrase: {idiom}\nMeaning: {meaning}'


print(RandomArtPiece.picture_link)
print(RandomArtPiece.picture_name)
print(RandomArtPiece.description)
print(RandomIdiom.print_idiom())