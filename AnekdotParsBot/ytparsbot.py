import hashlib

from aiogram import Dispatcher, Bot, types, utils
from aiogram.utils import executor
from aiogram.types import InputTextMessageContent, InlineQueryResultArticle
from youtube_search import YoutubeSearch

from config import TOKEN_API

def searcher(text):
    res = YoutubeSearch(text, max_results=10).to_dict()
    return res

# для получения результата в боте в строке набрать: @Lat_News_Bot желаемое, например-"смешное видео"
bot = Bot(token=TOKEN_API)
dp = Dispatcher(bot)


@dp.inline_handler()
async def inline_handler(query: types.InlineQuery):
    text = query.query or 'echo'
    links = searcher(text)

    articles = [types.InlineQueryResultArticle(
        id=hashlib.md5(f'{link["id"]}'.encode()).hexdigest(),
        title=f'{link["title"]}',
        url=f'https://www.youtube.com/watch?v={link["id"]}',
        thumb_url=f'{link["thumbnails"][0]}',
        input_message_content=types.InputTextMessageContent(
            message_text=f'https://www.youtube.com/watch?v={link["id"]}')
    ) for link in links]

    await query.answer(articles, cache_time=60, is_personal=True)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
# CTRL-C