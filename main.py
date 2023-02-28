import time
import json

from bs4 import BeautifulSoup
import requests


# News класс новостей содержит используем набор атрибутов со страницы сайта.
class News:
    def __init__(self, title, tag, pic, date):
        self.title = title
        self.tag = tag
        self.pic = pic
        self.date = date


# функция разыменовывает объект класса для получения всех атрибутов при выводе в JSON.
def obj_dict(News):
    return News.__dict__


# init содержит основной код программы.
# для начала загружается страница, при успешной загрузке текст страницы парсится BS'ом,
# после чего можно его разбивать на куски.
#
# Каждая собранная новость сохраняется в экземпляр новости, и добавляется в слайс новостей.
#
# Все новости в итоге сохраняются в JSON сериализацией из объекта класса.
def init():
    site = 'https://vvsu.ru/latests/'
    page = requests.get(site)
    if page.status_code != 200:
        print("получение страницы:", page.status_code)
        return

    soup = BeautifulSoup(page.text, "html.parser")

    print(soup)

    news = soup.find_all('div', class_='col-md-4 col-sm-6 item')
    print(news)

    # по большому счету сейчас в этих слайсах нет необходимости, сделаны для тестов.
    pics = []
    tags = []
    dates = []
    title = []

    # сохраним все новости в слайс all_news
    all_news = []

    for data in news:
        pic = data.find('img', class_='img-responsive')
        print(pic['src'])
        pics.append(pic['src'])
        title.append(data.find('a', class_='brand-link').text)
        print(data.find('a', class_='brand-link'))
        dates.append(data.find('p', class_='date').text)
        print(data.find('p', class_='date'))
        print(data.find('a',class_='label-success').text)
        tags.append(data.find('a',class_='label-success').text)
        singleNews = News(data.find('a', class_='brand-link').text, data.find('a',class_='label-success').text, pic['src'], data.find('p', class_='date').text)
        print(singleNews)
        all_news.append(singleNews)

    print(dates, "\n", pics, "\n", title, "\n", all_news)

    jsonList = json.dumps(all_news,default=obj_dict, ensure_ascii=False)
    print(jsonList)

    with open('json_data.json', 'w') as outfile:
        outfile.write(jsonList)

# Starting script here.
if __name__ == '__main__':
    init()
    time.sleep(2)
