import telebot
from telebot import types
from telebot.apihelper import ApiException
from bs4 import BeautifulSoup
import requests
import json
from words_scraper import Dictionary
import urllib.request
from idioms import IDIOMS
import random
from words_db import add_word

with open('token.json') as json_file:
    token = json.load(json_file)

API_TOKEN = token['API_TOKEN']

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
type /idiom. I can tell you what do different words mean in English. First, type /dict and after my reply write
  me the word you want to find in the dictionary. 
Moreover, I'm knowledgeable about classic art and can introduce you to it as well. Just type /art and I will show you 
some classic paintings.
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
    keyboard = types.ReplyKeyboardMarkup()
    dict_btn = types.KeyboardButton('/dict')
    art_btn = types.KeyboardButton('/art')
    idiom_btn = types.KeyboardButton('/idiom')
    add_word_btn = types.KeyboardButton('/add_word')
    learn_word_btn = types.KeyboardButton('/learn_word')
    keyboard.add(dict_btn, art_btn)
    keyboard.add(idiom_btn, add_word_btn, learn_word_btn)
    bot.send_chat_action(message.chat.id, 'typing')
    idiom = get_idiom()
    bot.send_message(message.chat.id, idiom, reply_markup=keyboard)


@bot.message_handler(commands=["art"])
def send_random_art(message):
    """/art"""
    keyboard = types.ReplyKeyboardMarkup()
    dict_btn = types.KeyboardButton('/dict')
    art_btn = types.KeyboardButton('/art')
    idiom_btn = types.KeyboardButton('/idiom')
    add_word_btn = types.KeyboardButton('/add_word')
    learn_word_btn = types.KeyboardButton('/learn_word')
    keyboard.add(dict_btn, art_btn)
    keyboard.add(idiom_btn, add_word_btn, learn_word_btn)
    bot.send_chat_action(message.chat.id, 'typing')
    art = get_art()
    bot.send_message(message.chat.id, art[2], reply_markup=keyboard)
    bot.send_photo(message.chat.id, art[1])

@bot.message_handler(commands=['dict'])
def dictionary_command(message):
    msg = bot.send_message(message.chat.id, "Just type a word and I explain you what does it mean. ")

    bot.register_next_step_handler(msg, retrieve_word)

@bot.message_handler(commands=['add_word'])
def ask_word(message):
    msg = bot.send_message(message.chat.id, "Ok, which word do you want me to add to favorites?")
    bot.register_next_step_handler(msg, save_word)



@bot.message_handler(commands=['learn_word'])
def random_from_fav(message):
    keyboard = types.ReplyKeyboardMarkup()
    dict_btn = types.KeyboardButton('/dict')
    art_btn = types.KeyboardButton('/art')
    idiom_btn = types.KeyboardButton('/idiom')
    add_word_btn = types.KeyboardButton('/add_word')
    learn_word_btn = types.KeyboardButton('/learn_word')
    keyboard.add(dict_btn, art_btn)
    keyboard.add(idiom_btn, add_word_btn, learn_word_btn)
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id, get_random_word(message.chat.id), reply_markup=keyboard)



def check_if_word_exists(word):
    if word is None or Dictionary(word.lower()).definitions() == Dictionary("@@@".lower()).definitions():
        return False
    else:
        return True

def save_word(message):
    keyboard = types.ReplyKeyboardMarkup()
    dict_btn = types.KeyboardButton('/dict')
    art_btn = types.KeyboardButton('/art')
    idiom_btn = types.KeyboardButton('/idiom')
    add_word_btn = types.KeyboardButton('/add_word')
    learn_word_btn = types.KeyboardButton('/learn_word')
    keyboard.add(dict_btn, art_btn)
    keyboard.add(idiom_btn, add_word_btn, learn_word_btn)
    bot.send_chat_action(message.chat.id, 'typing')
    file = "words_db.json"
    if check_if_word_exists(message.text):
        bot.send_message(message.chat.id, add_word((str(message.chat.id)), message.text, file), reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, "Oops, it seems that the word does not exist. Please, check spelling "
                                          "and try again.", reply_markup=keyboard)


def get_random_word(chat_id, db_file="words_db.json"):
    with open(db_file, "r") as json_file:
        data = json.load(json_file)
        chats = data["chat_id"]
        if str(chat_id) in chats.keys():
            random_word = random.choice(chats[str(chat_id)])
            return f"The word: " \
               f"{random_word}\n{Dictionary(random_word.lower()).definitions()}"
        else:
            return f"You don't have any saved words. First, /add_word to favorites to be able to learn the words"



def retrieve_word(message):
    keyboard = types.ReplyKeyboardMarkup()
    dict_btn = types.KeyboardButton('/dict')
    art_btn = types.KeyboardButton('/art')
    idiom_btn = types.KeyboardButton('/idiom')
    add_word_btn = types.KeyboardButton('/add_word')
    learn_word_btn = types.KeyboardButton('/learn_word')
    keyboard.add(dict_btn, art_btn)
    keyboard.add(idiom_btn, add_word_btn, learn_word_btn)
    bot.send_chat_action(message.chat.id, 'typing')
    if message.text is not None:
        if Dictionary(message.text.lower()).audio():
            audio = urllib.request.urlopen(Dictionary(message.text.lower()).audio()[0]).read()
            try:
                bot.send_message(message.chat.id, f'{Dictionary(message.text.lower()).definitions()}', reply_markup=keyboard)
                bot.send_audio(message.chat.id, audio)
            except ApiException and KeyError:
                bot.send_message(message.chat.id, "Sorry, I didn't find that word.", reply_markup=keyboard)
        else:
            try:
                bot.send_message(message.chat.id, f'{Dictionary(message.text.lower()).definitions()}', reply_markup=keyboard)
            except ApiException and KeyError:
                bot.send_message(message.chat.id, "Sorry, I can't find this word.", reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, "It doesn't seem to be a word.", reply_markup=keyboard)


bot.polling(none_stop=True)
