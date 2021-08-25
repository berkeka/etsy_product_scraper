import requests
import collections
import re
from bs4 import BeautifulSoup


class Scraper:
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    @classmethod
    def scrap(self, url):
        if self.url_is_valid(url):
            page = requests.get(url)
            # TO-DO Catch exception

            soup = BeautifulSoup(page.content, "html.parser")

            # Get item info column
            result = soup.find(id='listing-right-column')

            if result == None:
                return None, None, None, "Couldnt find product!"

            # Get img with the data-index 0
            image = result.find("img", attrs={'data-index' : 0})
            image_url = image['src']

            # Concentrate on text part
            text_info = result.find(id='listing-page-cart')

            # Find title of the product
            title_element = text_info.find("h1", attrs={'data-buy-box-listing-title' : True})
            name = title_element.text.strip()

            # Find price of the product
            price_info = text_info.find("div", attrs={'data-buy-box-region' : 'price'})
            price_text = price_info.find("p", class_='wt-text-title-03')

            # Remove span from p 
            for span_tag in price_text.findAll('span'):
                span_tag.replace_with('')

            price = price_text.text.strip()

            # Clean price text from currency and possible + sign
            cleaned_price = ''.join(char for char in list(price) if(char.isnumeric() or char == '.'))

            return name, image_url, cleaned_price, None
        else:
            return None, None, None, "Invalid_url!"

    @staticmethod
    def sanitize(string):
        print("a")

    @staticmethod
    def url_is_valid(url):
        if (url.startswith('https://www.etsy.com/') and (re.match(Scraper.regex, url) is not None)):
            return True
        else:
            return False
    