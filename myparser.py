import requests
import aiohttp
import asyncio
from bs4 import BeautifulSoup as BS
import csv

pages = []
url1 = 'https://www.citilink.ru/catalog/mobile/notebooks/'
req = requests.get(url1)
html = BS(req.content, 'html.parser')
pages_count = int(html.select('.last')[0].text)
id = 0


def write_csv(data):
    with open('citilink.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow((data['id'],
                         data['category'],
                         data['name'],
                         data['vin'],
                         data['color'],
                         data['price']))


async def load_page(num, url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url + '?available=1&status=55395790&p=' + str(num)) as response:
            pages.append(await response.text())


async def start_parsing(url, count):
    if url == 'https://www.citilink.ru/catalog/mobile/notebooks/':
        print("Адрес введен верно, начинаю парсинг")
        await asyncio.gather(
            *[load_page(num, url) for num in range(1, count)]
        )
        return True
    else:
        print("Проверьте правильность ардреса")
        return False


async def main():
    await start_parsing('https://www.citilink.ru/catalog/mobile/notebooks/', pages_count)


for r in pages:
    html = BS(r, 'html.parser')

    for element in html.select('.product_data__gtm-js'):
        try:
            title = element.select('.link_pageevents-js')[1].text.strip()

        except:
            title = element.select('.link_pageevents-js')[0].text.strip()

        try:
            price = element.select('.subcategory-product-item__price-num')[0].text.strip().replace(" ", "")

        except:
            price = "Цена не указана"

        a = title.split(',')
        try:
            category_name, vin, color = a
        except:
            continue
        b = category_name.split(" ", 1)
        category, name = b

        id += 1

        data = {'id': id,
                'category': category,
                'name': name,
                'vin': vin,
                'color': color,
                'price': price}

        write_csv(data)