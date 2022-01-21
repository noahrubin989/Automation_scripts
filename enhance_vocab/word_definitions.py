# A very simple practice script to scrape word definitions from the internet and place them in a text file
# Noah Rubin ~ 2021

import string
import requests
from bs4 import BeautifulSoup


def scrape_words(url, num_words=1000, start_letters='all'):
    """
    Scrapes words from https://www.vocabulary.com/lists/52473.
    You can control how many words (between 1 and 1000) that your wish to scrape
    You can also specify particular letters the word must start with (if you wish)
    """
    assert 0 < num_words <= 1000, 'Number of words must be between 1 and 1000'

    if start_letters == 'all':
        must_start_with = list(string.ascii_uppercase)
    else:
        must_start_with = [letter for letter in list(string.ascii_uppercase) if letter in start_letters]

    response = requests.get(url)
    soup = BeautifulSoup(response.content, features='lxml')
    all_words = soup.find_all('li', class_='entry learnable')[:num_words]

    records = []
    for word in all_words:
        curr_word = word.find('a', class_='word dynamictext').text.strip().title()

        # If the first letter of the word is something that we allow
        if curr_word[0] in must_start_with:
            curr_definition = word.find('div', class_='definition').text.strip()
            curr_sentence = word.find('div', 'example').text.strip()
            records.append((curr_word, curr_definition, curr_sentence))

    return records


def write_to_txt(data, filename):
    """Takes all the data and writes it to a text file. you can choose how many word definitions to write to the file"""

    with open(filename, 'w') as f:
        for word, definition, sentence in data:
            f.write(f"{word}:\n")

            # Convert the first letter of the sentence to capital
            f.write(f"Definition: {definition[0].upper() + definition[1:]}.\n")

            f.write(f"In a sentence: {sentence}\n")
            f.write('\n')


word_data = scrape_words(url='https://www.vocabulary.com/lists/52473')
write_to_txt(data=word_data, filename='cool_words.txt')
