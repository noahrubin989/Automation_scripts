# A quick and easy web scraping script to scrape quotes from azquotes.com
# Noah Rubin ~ 2022

import requests
from bs4 import BeautifulSoup


def get_all_quotes(pages_to_scrape=10):
    """
    A function to scrape 1000 quotes (at max) from azquotes.com
    Quotes are stored in a list of tuples
    """

    assert 0 < pages_to_scrape <= 10, 'Pages to scrape must be between 0-10'

    records = []
    for i in range(1, pages_to_scrape + 1):
        url = f'https://www.azquotes.com/top_quotes.html?p={i}'

        response = requests.get(url)
        soup = BeautifulSoup(markup=response.content, features='lxml')

        all_quotes = soup.find_all('div', class_='wrap-block')

        for quote in all_quotes:
            quote_text = quote.find('a', class_='title').text.strip()
            quote_author = quote.find('div', class_='author').text.strip()
            records.append((quote_text, quote_author))

    return records
