import requests
import collections
from bs4 import BeautifulSoup


class Scraper:
    @staticmethod
    def scrap(url):
        page = requests.get(url)

        soup = BeautifulSoup(page.content, "html.parser")

        # Get item info column
        result = soup.find(id='listing-right-column')
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

        return name, image_url, cleaned_price

    @staticmethod
    def sanitize(string):
        print("a")
    