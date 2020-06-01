import telebot
from bs4 import BeautifulSoup
import requests
import json

with open('token.json') as json_file:
    token = json.load(json_file)

API_TOKEN = token['API_TOKEN']

bot = telebot.TeleBot(API_TOKEN)

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:76.0) Gecko/20100101 Firefox/76.0'}


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Hi there, Im your Pocket Teacher bot.
I'm the bot that can teach you some things. For example, I can teach you some english idioms. To learn some just 
type /idiom (please don't be angry, sometimes I need to read it twice). 
Moreover, I am knowledgeable about classic art and can introduce you to it as well. Just type /art 
and I will show you some masterpieces. My creator, @dimazmn programs me to do things whenever he has free time, 
so I will be able to teach you more things in future. Stay tuned!\
""")


def get_idiom():

    url = 'https://randomword.com/idiom'

    source = requests.get(url).text

    soup = BeautifulSoup(source, 'html5lib')

    idiom = soup.find('div', {'id': 'random_word'}).text

    meaning = soup.find('div', {'id': 'random_word_definition'}).text

    return f'Phrase: {idiom}\nMeaning: {meaning}'


@bot.message_handler(commands=["idiom"])
def send_random_idiom(message):
    """/idiom"""

    idiom = get_idiom()

    msg = bot.send_message(message.chat.id, idiom)

    bot.register_next_step_handler(msg, send_idiom)


def send_idiom(message):
    if message.text == "/idiom":
        bot.send_message(message.chat.id, get_idiom())


def get_art():

    url = 'https://random-ize.com/random-art-gallery/'

    source = requests.get(url,  headers=headers).text

    soup = BeautifulSoup(source, 'html5lib')

    picture_link = 'https://random-ize.com' + soup.find('img')['src']

    picture_name = soup.find('img')['alt']

    description = soup.find_all('center')[1].div.text

    return f'{picture_name}\n{picture_link}\n{description}'


@bot.message_handler(commands=["art"])
def send_random_idiom(message):
    """/art"""

    art = get_art()

    msg = bot.send_message(message.chat.id, art)

    bot.register_next_step_handler(msg, send_art)


def send_art(message):
    if message.text == "/art":
        bot.send_message(message.chat.id, get_art())


bot.polling(none_stop=True)
