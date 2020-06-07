import telebot
from beautiful_soup_proj import OlxApartmetAds


API_TOKEN = '1060549504:AAFwWKDRJgyhnhsL9f0vDFVoRSOtDbzg1ck'

bot = telebot.TeleBot(API_TOKEN)

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:76.0) Gecko/20100101 Firefox/76.0'}




@bot.message_handler(commands=['ads'])
def ads_message(message):
    ads = OlxApartmetAds()
    for ad in ads.ad_generator():
        if ad[1] <= 1350:
            bot.send_message(message.chat.id, text=f'Total price:{ad[1]} \n{ad[0]}')


@bot.message_handler(func=lambda message: message.text == "page 2")
def page_2(message):
    ads = OlxApartmetAds(2)
    for ad in ads.ad_generator():
        if ad[1] <= 1350:
            bot.send_message(message.chat.id, text=f'Total price:{ad[1]} \n{ad[0]}')


@bot.message_handler(func=lambda message: message.text == "page 3")
def page_3(message):
    ads = OlxApartmetAds(3)
    for ad in ads.ad_generator():
        if ad[1] <= 1350:
            bot.send_message(message.chat.id, text=f'Total price:{ad[1]} \n{ad[0]}')

@bot.message_handler(func=lambda message: message.text == "page 4")
def page_4(message):
    ads = OlxApartmetAds(4)
    for ad in ads.ad_generator():
        if ad[1] <= 1350:
            bot.send_message(message.chat.id, text=f'Total price:{ad[1]} \n{ad[0]}')

@bot.message_handler(func=lambda message: message.text == "page 5")
def page_5(message):
    ads = OlxApartmetAds(5)
    for ad in ads.ad_generator():
        if ad[1] <= 1350:
            bot.send_message(message.chat.id, text=f'Total price:{ad[1]} \n{ad[0]}')

@bot.message_handler(func=lambda message: message.text == "page 6")
def page_6(message):
    ads = OlxApartmetAds(6)
    for ad in ads.ad_generator():
        if ad[1] <= 1350:
            bot.send_message(message.chat.id, text=f'Total price:{ad[1]} \n{ad[0]}')

@bot.message_handler(func=lambda message: message.text == "page 7")
def page_7(message):
    ads = OlxApartmetAds(7)
    for ad in ads.ad_generator():
        if ad[1] <= 1350:
            bot.send_message(message.chat.id, text=f'Total price:{ad[1]} \n{ad[0]}')

@bot.message_handler(func=lambda message: message.text == "page 8")
def page_8(message):
    ads = OlxApartmetAds(8)
    for ad in ads.ad_generator():
        if ad[1] <= 1350:
            bot.send_message(message.chat.id, text=f'Total price:{ad[1]} \n{ad[0]}')



bot.polling(none_stop=True)

