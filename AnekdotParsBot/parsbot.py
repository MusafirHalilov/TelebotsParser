import random
import time
from bs4 import BeautifulSoup as BS
import requests
import telebot
from config import TOKEN_API, channel_id


URL = 'https://anekdot.ru/last/good/'
HEADERS = {
    'User-Agent':
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Accept': '*/*'
}
r = requests.get(URL)
soup = BS(r.text, 'html.parser')
anekdots = soup.find_all('div', class_='text')
clear_anekdots = [c.text for c in anekdots]
print(clear_anekdots)

# def parser(url): # парсит сайт с анекдотами и выводит их в список
#     # r = requests.get(url)
#     r = requests.get(url, headers=HEADERS)
#     soup = BS(r.text, 'html.parser')
#     anekdots = soup.find_all('div', class_='text')
#     return [c.text for c in anekdots]

# list_of_jokes = parser(URL)
# random.shuffle(list_of_jokes)

# bot = telebot.TeleBot(TOKEN_API)

# for joke in list_of_jokes:
#     bot.send_message(channel_id, joke) # загрузка всех анекдотов в телеграм-канал
#     # Делаем паузу в сек
#     time.sleep(3)
# bot.send_message(channel_id, "Анекдоты закончились :-(") 


# @bot.message_handler(commands=['start'])
# def hello(message):
#     bot.send_message(message.chat.id, 'Привет! Чтобы посмеяться введи цифру 1:')

# @bot.message_handler(content_types=['text'])
# def jokes(message):
#     if message.text.lower() == '1':
#         bot.send_message(message.chat.id, list_of_jokes[0])   
#         # bot.send_message(chat_id=channel_id, text=list_of_jokes[0]) # одновременно постит в канал    
#         del list_of_jokes[0]
#     else:
#         bot.send_message(message.chat.id, 'Введи цифру 1')


# bot.polling()