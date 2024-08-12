from bs4 import BeautifulSoup as BS
import requests


base_url = 'https://anekdot.ru/last/good/'
HEADERS = {
    'User-Agent':
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Accept': '*/*'
}

def parse(url):
    session = requests.Session()
    response = session.get(url, headers=HEADERS)
    soup = BS(response.content, 'html.parser')
    items = soup.find_all('div', class_='text')
    return [c.text for c in items]
    # clear_anekdots = [c.text for c in items]
    # print(clear_anekdots)


# print(parse(url=base_url))