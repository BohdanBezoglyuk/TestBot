import asyncio
import logging
import requests
import xml.etree.ElementTree as ET
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message

from config import token  

bot = Bot(token=token)
dp = Dispatcher()

RSS_FEED_URL = 'https://www.unian.ua/rss'

def get_top_ua_news():
    try:
        response = requests.get(RSS_FEED_URL)
        response.raise_for_status()
        root = ET.fromstring(response.content)

        news_list = []
        for item in root.findall('./channel/item')[:5]:
            title = item.find('title').text
            link = item.find('link').text
            news_list.append(f"{title}\n{link}")

        if not news_list:
            return ['На жаль, не вдалося знайти новини.']

        return news_list
    except Exception as e:
        print(f"Помилка: {e}")
        return ['Сталася помилка при отриманні новин.']

@dp.message(CommandStart())
async def cmd_start(message: Message):
    news = get_top_ua_news()
    reply_text = "\n\n".join(news)
    await message.answer(f"Привіт! Ось топ-5 українські новини на сьогодні:\n\n{reply_text}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
