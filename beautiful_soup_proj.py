from bs4 import BeautifulSoup
import requests


source = requests.get('https://www.olx.pl/nieruchomosci/mieszkania/wynajem/wroclaw/'
                      '?search%5Bfilter_float_price%3Afrom%5D=700&search%5Bfilter_float_price%'
                      '3Ato%5D=1300&search%5Bfilter_enum_rooms%5D%5B0%5D=one&search%5Border%5D=created_at%3Adesc').text


soup = BeautifulSoup(source, 'lxml')

adverts = soup.find_all('div', class_='offer-wrapper')



def filter_price(string):
    return ''.join(filter(str.isdigit, string))


def make_ad_list():
    ads = []
    for ad in adverts:
        ad_link = ad.a['href']
        ad_price = ad.find('p', class_='price').text
        ads.append((ad_link, filter_price(ad_price)))
    return ads

def ad_bill(link):
    advert_source = requests.get(link).text
    advert_soup = BeautifulSoup(advert_source, 'html5lib')
    advert_detail = advert_soup.find_all('strong', class_='offer-details__value')
    lst = []
    for detail in advert_detail:
        detail_value = detail.text
        lst.append(detail_value)
    return filter_price(lst[-1])


def is_olx_link(link):
    if link.split('/')[2] == 'www.olx.pl':
        return True


def ad_generator():
    for link in make_ad_list():
        if is_olx_link(link[0]):
            yield (link[0], (int(link[1]) + int(ad_bill(link[0]))))


def gen_func():
    for ad in ad_generator():
        return (f'{ad[0]}, {ad[1]}')


