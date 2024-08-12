import asyncio
from aiogram import Bot, Dispatcher, executor, types
import time
import requests
from bs4 import BeautifulSoup as BS
from aiogram import types
from youtube_search import YoutubeSearch
from aiogram.types import Message, MediaGroup, InputMediaDocument
from aiogram.dispatcher.filters import Text
import random

from config import TOKEN_API, channel_id


# # парсер сайта с анекдотами и постит их в Телеграм-канале
URL = 'https://anekdot.ru/last/good/'
HEADERS = {
    'User-Agent':
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Accept': '*/*'
}

def parser(url): 
    # r = requests.get(url)
    r = requests.get(url, headers=HEADERS)
    soup = BS(r.text, 'html.parser')
    anekdots = soup.find_all('div', class_='text')
    return [c.text for c in anekdots]

list_of_jokes = parser(URL)
random.shuffle(list_of_jokes)


# # парсер ссылок на видео с ютуба
search_query = "Смешное видео, приколы, анекдоты" # "Приколы с котами и собаками" # "Том и Джерри" #   

results = YoutubeSearch(search_query, max_results=20).to_dict()

output_res = "YouTube Search Results:\n\n"
for result in results:
    title = result["title"]
    video_id = result["id"]
    link = f"https://www.youtube.com/watch?v={video_id}"
    output_res += f"{title}\n{link}\n\n"


bot = Bot(token=TOKEN_API)
dp = Dispatcher(bot)


# # загрузка всех анекдотов в телеграм-канал
async def news_every():
    for joke in list_of_jokes:
        await bot.send_message(channel_id, joke, disable_notification=True)          
        # Делаем паузу в сек
        time.sleep(3)
    # await asyncio.sleep(40)
    # await bot.send_message(channel_id, "А смешного видео ХОЧЕШЬ? Перейди по ссылке: https://t.me/Lat_News_Bot и отправь боту цифру: '1'")
    # await bot.send_message(chat_id=channel_id, text=output_res) # одновременно постит в канал результаты поиска видео на ютубе

# # постит результаты поиска видео на ютубе в чат пользователя бота 
@dp.message_handler(commands=['start'])
async def hello(message: types.Message):
    await bot.send_message(message.chat.id, 'Привет! Чтобы посмеяться введи цифру 1:')
    
@dp.message_handler(content_types=['text'])
async def jokes(message: types.Message):
    if message.text.lower() == '1':
        await bot.send_message(message.chat.id, output_res)   
        # await bot.send_message(chat_id=channel_id, text=output_res) # одновременно постит в канал    
        # del output_res
    else:
        await bot.send_message(message.chat.id, 'Введи цифру 1')
  

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(news_every())
    executor.start_polling(dp, skip_updates = True)