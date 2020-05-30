import telegram
from telegram.ext import Updater
import logging
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from beautiful_soup_proj import ad_generator

bot = telegram.Bot(token='1150644309:AAF_fAyfPbV2jZKbg9Y0oEqi8oZhMXlHMaM')
updater = Updater(token='1150644309:AAF_fAyfPbV2jZKbg9Y0oEqi8oZhMXlHMaM', use_context=True)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

logger = logging.getLogger()
logger.setLevel(logging.ERROR)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hi there! I'm a bot that can send you "
                                                                    "ads from OLX.pl. At the time my functionality is "
                                                                    "very limited, so I can send you only ads that my"
                                                                    "creator @dimazmn told me to send. "
                                                                    "Type /ads to see the last created apartment "
                                                                    "related "
                                                                    "ads that show total calculated price "
                                                                    "and its link.")




start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)


def caps(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Smth wrong')


caps_handler = CommandHandler('caps', caps)
dispatcher.add_handler(caps_handler)

def send_link(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="https://dictionary.cambridge.org/dictionary/learner-english/across-the-board")

send_link_handler = CommandHandler('send_link', send_link)
dispatcher.add_handler(send_link_handler)

def ads(update, context):
    for ad in ad_generator():
        context.bot.send_message(chat_id=update.effective_chat.id, text=f'Total price: {ad[1]}\n'
                                                                        f'Link: {ad[0]}\n')


ads_handler = CommandHandler('ads', ads)
dispatcher.add_handler(ads_handler)


updater.start_polling()

