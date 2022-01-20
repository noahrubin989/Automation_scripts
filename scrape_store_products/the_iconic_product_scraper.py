import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import date


def acquire_product_links(num_pages, brand_name):
    """Gets all the product links for a particular brand for the first {num_pages} pages"""
    base = 'https://www.theiconic.com.au'

    product_links = []
    for i in range(1, num_pages + 1):
        url = f'https://www.theiconic.com.au/{brand_name}/?page={i}'
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'lxml')

        # This is a ResultSet object
        all_products = soup.find_all('div', class_='product small-6 medium-4 large-3 columns')
        # print(type(all_products))

        # Look inside each div class (each product) and get get the a tag and get the product and href
        for item in all_products:
            for link in item.find_all('a', href=True):
                if link.get('href') != '#':
                    # ie it won't show https://www.theiconic.com.au/# which is good
                    product_links.append(f"{base}{link.get('href')}")

    return product_links


def collect_all_records(list_of_links, brand_name):
    """For each url it finds, it places all the product info inside a tuple, which gets placed inside a big list"""
    records = []
    for individual_link in list(set(list_of_links)):
        r = requests.get(individual_link)
        soup = BeautifulSoup(r.content, 'lxml')

        try:
            product_title = soup.find('h1', class_='product-title').text.strip()
            price = soup.find('span', class_='price').text.strip()
            if price is None:
                price = soup.find('span', class_='price final').text.strip()  # THE SALE PRICE IN RED
            records.append((product_title, price, individual_link, brand_name))

        except AttributeError:
            print(f"The following link has caused a problem: {individual_link}")

    return records


def create_dataframe(list_of_records):
    """Places all records in a pandas dataframe"""
    data = pd.DataFrame(data=list_of_records, columns=['Product', 'Price', 'URL', 'brand'])
    data['Date'] = date.today().strftime("%d/%m/%Y")
    return data


all_records = []
brands = ['stussy', 'adidas-originals', 'nike', 'polo-ralph-lauren']
for brand in brands:
    brand_products = acquire_product_links(num_pages=6, brand_name=brand)
    product_specs = collect_all_records(brand_products, brand)
    all_records.extend(product_specs)

df = create_dataframe(all_records)
df.to_csv('scraped_data.csv', index=False)
