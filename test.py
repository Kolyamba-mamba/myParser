# Тут будут тесты
import asyncio
from myparser import start_parsing


async def test_sitilink_notenook():
    await start_parsing('https://www.citilink.ru/catalog/mobile/notebooks/', 3)


async def test_sitilink_catalog():
    await start_parsing('https://www.citilink.ru/catalog/mobile/', 3)


async def test_wrong_url():
    await start_parsing('https://www.google.ru/', 4)


asyncio.run(test_sitilink_notenook())
asyncio.run(test_sitilink_catalog())
asyncio.run(test_wrong_url())