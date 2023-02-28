import time
import json
import csv
import re

import pandas as pn

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

    # по большому счету в этих слайсах нет необходимости, сделаны для тестов.
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
        print(data.find('a', class_='label-success').text)
        tags.append(data.find('a', class_='label-success').text)
        singleNews = News(data.find('a', class_='brand-link').text, data.find('a', class_='label-success').text,
                          pic['src'], data.find('p', class_='date').text)
        print(singleNews)
        all_news.append(singleNews)

    print(dates, "\n", pics, "\n", title, "\n", all_news)
    # ensure_ascii=False позволяет записывать русские символы в файл
    jsonList = json.dumps(all_news, default=obj_dict, ensure_ascii=False)
    print(jsonList)

    with open('json_data.json', 'w') as outfile:
        outfile.write(jsonList)


# regular исследование регулярных выражений
def regular():
    # найдём знак '@'.
    # '\w' - любая буква(то, что может быть частью слова);
    # '+' - не менее 1 знака и более;
    # Ищем знак '.'
    text = 'glebik000@gmail.com, glebov.evgeniy1@edu.vvsu.ru, glebik000@mail.ru, test-email@ya.list.ru'
    result = re.findall(r'@\w+.\w+.\w+', text)
    print(result)

    # Проверка корректности вводимого пароля
    correct = 'TESTpass!1'
    incorrect = 'testpas2'

    # (?=.*[0-9]) - строка содержит хотя бы одно число;
    # (?=.*[a-z]) - строка содержит хотя бы одну латинскую букву в нижнем регистре;
    # (?=.*[A-Z]) - строка содержит хотя бы одну латинскую букву в верхнем регистре;
    # [0-9a-zA-Z@#%^!$]{8,} - строка состоит не менее, чем из 8 перечисленных символов.
    result = re.findall(r'^(?=.*[0-9].*)(?=.*[a-z].*)(?=.*[A-Z].*)[0-9a-zA-Z@#%^!$]{8,}', correct)
    print(result)

    result = re.findall(r'^(?=.*[0-9].*)(?=.*[a-z].*)(?=.*[A-Z].*)[0-9a-zA-Z@#%^!$]{8,}', incorrect)
    print(result)

    # Разбор строки по разделителям
    text = 'asd,sadf,sADF;sdfasxcl asddcaaed;saxadf,aszxa,aszx'
    # \s - любой пробелльный символ;
    # [] - один из символов в скобках.
    result = re.split(r'[;,\s]', text)
    print(result)

    new_data = pn.read_csv('phones_data.csv')

    # Преобразование даты
    counter = 0
    for i in new_data['release_date']:
        if counter > 10:
            break
        result = re.sub(r'[-]', '.', str(i))
        counter = counter + 1
        print(result)

    print(new_data['release_date'])

    # Преобразование числа
    counter = 0
    for i in new_data['best_price']:
        if counter > 10:
            break
        result = re.sub(r'[.]', ',', str(i))
        counter = counter + 1
        print(result)

    print(new_data['best_price'])


def formatter():
    # Преобразование текстового файла в формат csv
    saveData = []
    with open("formatter.txt", "rt") as inFile:
        rawData = inFile.readlines()[0:10]
        for line in rawData:
            # Присутствуют строковые значения int(v) замнен на str(v)
            row = [str(v) for v in line.split('\t')]
            # [:-1] удаление конца строки (\n)
            saveData.append(row[:-1])

    # Создание, запись с заполнением и сохранение файла csv, разделитель ","
    with open("formatter.csv", "wt", newline='') as csvOut:
        # Создаем объект, делиметр ","
        csvWriter = csv.writer(csvOut, delimiter=",")
        # Запись строк
        for row in saveData:
            csvWriter.writerow(row)

    # Преобразование csv файла в формат json

    myData = {}

    with open("formatter.csv", "rt") as csvfile:
        csvRead = csv.DictReader(csvfile)
        for rows in csvRead:
            # Ключ словаря
            myKey = rows['time']
            # заполнение элементов словаря по ключу
            myData[myKey] = rows

    # Создание, запись и сохранение файла формата json
    with open("formatter.json", "wt", encoding="utf-8") as jsonfile:
        # ensure_ascii=False позволяет записывать русские символы в файл
        jsonfile.write(json.dumps(myData, indent=4, ensure_ascii=False))


# Starting script here.
if __name__ == '__main__':
    init()
    time.sleep(2)
    regular()
    time.sleep(2)
    formatter()
    time.sleep(2)
