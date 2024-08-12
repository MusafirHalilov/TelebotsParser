# # парсер + бот, который парсит ютуб и сайт с анекдотами и постит результат сразу в телеграмм-канал 
import random
import time
from bs4 import BeautifulSoup as BS
import requests

from youtube_search import YoutubeSearch
import telebot
from telebot import types

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


# # бот, который постит анедоты и результат поиска с ютуб сразу в телеграмм-канал 
bot = telebot.TeleBot(token=TOKEN_API)


# # загрузка всех анекдотов в телеграм-канал
for joke in list_of_jokes:
    bot.send_message(channel_id, joke) 
    # Делаем паузу в сек
    time.sleep(3)
# bot.send_message(channel_id, "А смешного видео ХОЧЕШЬ? Перейди по ссылке в бота: https://t.me/Lat_News_Bot и отправь ему: '1'")


# # постит результаты поиска видео на ютубе в чат пользователя бота 
@bot.message_handler(commands=['start'])
def hello(message):
    bot.send_message(message.chat.id, 'Привет! Чтобы посмеяться введи цифру 1:')
    
@bot.message_handler(content_types=['text'])
def jokes(message):
    if message.text.lower() == '1':
        bot.send_message(message.chat.id, output_res)   
        # bot.send_message(chat_id=channel_id, text=output_res) # одновременно постит в канал    
        # del output_res
    else:
        bot.send_message(message.chat.id, 'Введи цифру 1')

bot.polling()


# # бот с кнопками постит в чат пользователя видео с ютуба
# @bot.message_handler(commands=[''])
# def button(message):
#     markup = types.InlineKeyboardMarkup(row_width=2)
#     item = types.InlineKeyboardButton('Видео', callback_data='question_1')
#     item2 = types.InlineKeyboardButton('Video2', callback_data='goodbye')
#     markup.add(item, item2)
#     bot.send_message(message.chat.id, 
#                      "Привет! Чтобы посмотреть смешное видео с Youtube жми кнопку 'Видео'", 
#                      reply_markup=markup)

# @bot.callback_query_handler(func=lambda call:True)
# def callback(call):
#     if call.message:
#         if call.data == 'question_1':
#             bot.send_message(call.message.chat.id, output_res)
#         elif call.data == 'goodbye':
#             bot.send_message(call.message.chat.id, 'Poka Drug')

# bot.polling()