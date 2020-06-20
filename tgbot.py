import telebot
from telebot.apihelper import ApiException
from bs4 import BeautifulSoup
import requests
<<<<<<< HEAD

API_TOKEN = '1150644309:AAF_fAyfPbV2jZKbg9Y0oEqi8oZhMXlHMaM'
=======
import json
from words_scraper import Dictionary
import urllib.request
from idioms import IDIOMS
import random

with open('token.json') as json_file:
    token = json.load(json_file)

API_TOKEN = token['API_TOKEN']
>>>>>>> 0b1543fb6cfd4f72555cef8823ffc248e4cd5acf

bot = telebot.TeleBot(API_TOKEN)

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:76.0) Gecko/20100101 Firefox/76.0'}


def get_idiom():
    idiom = random.choice(IDIOMS)
    return f'Phrase: \n{idiom[0]}\nMeaning:\n{idiom[1]}'


def get_art():
    url = 'https://random-ize.com/random-art-gallery/'
    source = requests.get(url,  headers=headers).text
    soup = BeautifulSoup(source, 'html5lib')
    picture_link = 'https://random-ize.com' + soup.find('img')['src']
    picture_name = soup.find('img')['alt']
    description = soup.find_all('center')[1].div.text
    # return f'{picture_name}\n{picture_link}\n{description}'
    return [picture_name, picture_link, description]


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(
        telebot.types.InlineKeyboardButton(
            'Contact with author', url='telegram.me/dimazmn'
        )
    )
    keyboard.row(telebot.types.InlineKeyboardButton('dictionary', callback_data='get-Dict'))
    bot.send_message(message.chat.id, """\
Hi there, I'm Pocket Teacher bot.
I'm the bot who can teach you various things. For example, I can teach you some english idioms. To learn some of them just 
type /idiom. I can tell you what do different words mean in English. First, type /dict and then the word. 
Moreover, I'm knowledgeable about classic art and can introduce you to it as well. Just type /art and I will show you 
some masterpieces.
My creator, @dimazmn programs me to do things whenever he has free time, 
so I will be able to teach you more things in future. Stay tuned!\
""", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback(query):
    data = query.data
    if data.startswith('get-'):
        get_ex_callback(query)

def get_ex_callback(query):
   bot.answer_callback_query(query.id)
   dictionary_command(query.message)


@bot.message_handler(commands=["idiom"])
def send_random_idiom(message):
    """/idiom"""
    bot.send_chat_action(message.chat.id, 'typing')
    idiom = get_idiom()
    bot.send_message(message.chat.id, idiom)


@bot.message_handler(commands=["art"])
def send_random_art(message):
    """/art"""
    bot.send_chat_action(message.chat.id, 'typing')
    art = get_art()
    bot.send_message(message.chat.id, art[2])
    bot.send_photo(message.chat.id, art[1])

@bot.message_handler(commands=['dict'])
def dictionary_command(message):
    msg = bot.send_message(message.chat.id, "Just type a word and I tell you what does it mean. "
                                            "Please use lowercase unless it's not a proper noun")
    bot.register_next_step_handler(msg, retrieve_word)


def retrieve_word(message):
            bot.send_chat_action(message.chat.id, 'typing')
            if Dictionary(message.text).audio():
                audio = urllib.request.urlopen(Dictionary(message.text).audio()[0]).read()
                try:
                    bot.send_message(message.chat.id, f'{Dictionary(message.text).definitions()}')
                    bot.send_audio(message.chat.id, audio)
                except ApiException and KeyError:
                    bot.send_message(message.chat.id, "Sorry, I didn't find that word.")
            else:
                try:
                    bot.send_message(message.chat.id, f'{Dictionary(message.text).definitions()}')
                except ApiException and KeyError:
                    bot.send_message(message.chat.id, "Sorry, I didn't find that word.")


bot.polling(none_stop=True)
