from bs4 import BeautifulSoup
import requests

# uu = 'https://www.olx.pl/nieruchomosci/mieszkania/wynajem/wroclaw/' \
#      '?search%5Bfilter_float_price%3Ato%5D=1300&search%5Bfilter_enum_rooms%5D%5B0%5D=one&' \
#      'search%5Border%5D=filter_float_price%3Aasc'
#
# filt = ['filter_float_price', 'created_at']

class OlxApartmetAds:

    def __init__(self, page=None):
        self.page = page

        self.url = 'https://www.olx.pl/nieruchomosci/mieszkania/wynajem/wroclaw/' \
                   '?search%5Bfilter_float_price%3Ato%5D=1300&search%5Bfilter_enum_rooms%5D%5B0%5D=one&' \
                   'search%5Border%5D=created_at%3Aasc&'

        self.url = self.url + f'page={page}'

        self.source = requests.get(self.url).text

        self.soup = BeautifulSoup(self.source, 'lxml')

        self. adverts = self.soup.find_all('div', class_='offer-wrapper')


    @staticmethod
    def filter_price(string):
        return ''.join(filter(str.isdigit, string))


    def make_ad_list(self):
        ads = []
        for ad in self.adverts:
            ad_link = ad.a['href']
            ad_price = ad.find('p', class_='price').text
            ads.append((ad_link, self.filter_price(ad_price)))
        return ads

    def ad_bill(self, link):
        advert_source = requests.get(link).text
        advert_soup = BeautifulSoup(advert_source, 'html5lib')
        advert_detail = advert_soup.find_all('strong', class_='offer-details__value')
        lst = []
        for detail in advert_detail:
            detail_value = detail.text
            lst.append(detail_value)
        try:
            return self.filter_price(lst[-1])
        except IndexError:
            return self.filter_price(lst[0])

    @staticmethod
    def is_olx_link(link):
        if link.split('/')[2] == 'www.olx.pl':
            return True

    def ad_generator(self):
        for link in self.make_ad_list():
            if self.is_olx_link(link[0]):
                print (link[0], (int(link[1]) + int(self.ad_bill(link[0]))))


if __name__ == '__main__':

    ads = OlxApartmetAds()

    print(ads.ad_generator())



