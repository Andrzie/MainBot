import requests    # для запросов
import json
import telebot
from bs4 import BeautifulSoup   # для парсинга


TOKEN = '5251667100:AAFHrW9oxlwxIX6AUvndIcAqTOUYqgYk84w'
bot = telebot.TeleBot(TOKEN)

BANK_API = 'http://www.nbrb.by/API/ExRates/Rates?Periodicity=0'
response = requests.get(BANK_API)                   #requests -- запрос
print(response.text)


def get_money():
    url = 'http://www.nbrb.by/API/ExRates/Rates?Periodicity=0'
    response = requests.get(url).json()

    for elem in list(response):
        if elem['Cur_Abbreviation'] == 'USD':
            usd_price = elem['Cur_OfficialRate']

        if elem['Cur_Abbreviation'] == 'EUR':
            eur_price = elem['Cur_OfficialRate']

    return f'cost of one BYN today - {usd_price} USD, {eur_price} EUR'


def get_weather():
    response = requests.get('http://api.openweathermap.org/data/2.5/weather?q=Minsk&units=metric&appid = 8ad74868a4a9e221ca9bf421e4abfa80')
    data = json.loads(response.text)
    weather = data['main']['temp']
    city = data['name']
    return f'В городе {city}, такая погода - {weather}'

link_for_parse = 'https://afisha.relax.by/kino/minsk/'   # ссылка, откуда возьмём данные
page = requests.get(link_for_parse)   # тут GET запрос на ссылку
soup = BeautifulSoup(page.text, "html.parser")
allItem = soup.findAll('a', {'class':'b-afisha_blocks-strap_item_lnk_txt link'})

for iter in allItem:
    print(iter.get_text())


@bot.message_handler(commands=['money'])
def start_message(message):
    bot.send_message(message.chat.id, get_money())


@bot.message_handler(commands=['weather'])
def start_message(message):
    bot.send_message(message.chat.id, get_weather())


bot.polling()