import requests
import aiohttp
import asyncio
from bs4 import BeautifulSoup as BS
import csv

pages = []
url = 'https://www.citilink.ru/catalog/mobile/notebooks/'
req = requests.get(url)
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


async def load_page(num):
    async with aiohttp.ClientSession() as session:
        async with session.get(url + '?available=1&status=55395790&p=' + str(num)) as response:
            pages.append(await response.text())


async def main():
    # Schedule three calls *concurrently*:
    await asyncio.gather(
        *[load_page(num) for num in range(1, pages_count)]
    )


asyncio.run(main())

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

        print(data)
