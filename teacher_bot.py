import telegram
from telegram.ext import Updater
import logging
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from teacher_bot_tasks import RandomIdiom, RandomArtPiece


class PocketTeacherBot:

    bot = telegram.Bot(token='1150644309:AAF_fAyfPbV2jZKbg9Y0oEqi8oZhMXlHMaM')
    updater = Updater(token='1150644309:AAF_fAyfPbV2jZKbg9Y0oEqi8oZhMXlHMaM', use_context=True)
    dispatcher = updater.dispatcher
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    logger = logging.getLogger()
    logger.setLevel(logging.ERROR)

    def start(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Hi there! I'm a bot that can teach you some"
                                                                    "things. I can teach you some english "
                                                                    "idioms and phrases. To do that, type /idiom. "
                                                                    "I am knowledgeable about classic art and can "
                                                                    "introduce you to it as well. Just type /art "
                                                                    "and I will show you some masterpieces. "
                                                                    "My author, @dimazmn teaches me things, so "
                                                                    "I will be able to teach you more things")





    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    def echo(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(echo_handler)


    def caps(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text='Smth wrong')


    caps_handler = CommandHandler('caps', caps)
    dispatcher.add_handler(caps_handler)


    def art(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text=f'{RandomArtPiece.picture_name}\n '
                                                                    f'{RandomArtPiece.picture_link}\n'
                                                                    f'{RandomArtPiece.description}')


    art_handler = CommandHandler('art', art)
    dispatcher.add_handler(art_handler)


    def idiom(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text=f'{RandomIdiom.print_idiom()}')

    idiom_handler = CommandHandler('idiom', idiom)
    dispatcher.add_handler(idiom_handler)


    updater.start_polling()

