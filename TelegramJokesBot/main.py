import requests
import random
import telebot
from telebot import types
from bs4 import BeautifulSoup as b

# Основная ссылка на сайт, который будет парситься
URL = 'https://www.anekdot.ru'
# Уникальный токен для доступа к боту
API_KEY = 'КЛЮЧ АПИ'

bot = telebot.TeleBot(API_KEY)

# Функция, считывающая названия категорий с сайта и соответствующие им пути
def GetCategories(url, numcat):
    r = requests.get(URL)
    soup = b(r.text, 'html.parser')

    NPanel = soup.find('ul', id='topmenu')
    category = NPanel.find_all('a')

    CategoryName = []
    CategoryHref = []
    TelegramMenu = []
    iterator = 0

    for i in category:
        buff = str(i)
        buff = buff.split('"')
        CategoryHref.append(buff[1])
        CategoryName.append(i.text)


        if i.text == 'Анекдоты' or i.text == 'Истории' or i.text == 'Фразы' or i.text == 'Стишки':
            TelegramMenu.append(iterator)

        iterator = iterator + 1

    changed_URL = url + CategoryHref[TelegramMenu[numcat]]
    return changed_URL

# Функция, считывающая текст с сайта и формирующая список с отдельными друг от друга анекдотами
def parser(url):
    r = requests.get(url)
    soup = b(r.text, 'html.parser')
    anekdots = soup.find_all('div', class_ = 'text')
    clear_anekdots = [c.text for c in anekdots]
    return clear_anekdots

# При вводе и отправке боту команды /start, запускается функция def button(message)
@bot.message_handler(commands=['start'])
# Функция, реализующая кнопки главного меню у бота
def button(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item1 = types.KeyboardButton('Анекдот')
    item2 = types.KeyboardButton('История')
    item3 = types.KeyboardButton('Фраза')
    item4 = types.KeyboardButton('Стих')
    item5 = types.KeyboardButton('Информация о боте')
    markup.add(item1, item2, item3, item4, item5)

    bot.send_message(message.chat.id, 'Здравствуйте! Вас приветствует бот шуток!', reply_markup=markup)


@bot.message_handler(content_types = ['text'])
# Функция, реализующая несколько подменю и функционал кнопок в этих подменю
def bot_message(message):
    # Переменные, необходимые для ограничения повторов шуток
    FirstVisitAnekdots = True
    FirstVisitStories = True
    FirstVisitAphorisms = True
    FirstVisitPoems = True

    # Если чат с ботом происходит в личных сообщениях, а не через сторонние группы:
    if message.chat.type == 'private':

        if message.text == 'Анекдот':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('Случайный Анекдот')
            item2 = types.KeyboardButton('Назад')
            markup.add(item1, item2)

            bot.send_message(message.chat.id, 'Анекдот', reply_markup=markup)

            NewURL = GetCategories(URL, 0)
            print('NewURL ', NewURL)

        elif message.text == 'Случайный Анекдот':
            NewURL = GetCategories(URL, 0)
            print('NewURL ', NewURL)

            if FirstVisitAnekdots == True:
                list_of_jokes = parser(NewURL)
                random.shuffle(list_of_jokes)
                FirstVisitAnekdots = False

            if len(list_of_jokes) < 1:
                list_of_jokes = parser(NewURL)
                random.shuffle(list_of_jokes)

            bot.send_message(message.chat.id, list_of_jokes[0])
            del list_of_jokes[0]

        elif message.text == 'История':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('Случайная История')
            item2 = types.KeyboardButton('Назад')
            markup.add(item1, item2)

            bot.send_message(message.chat.id, 'История', reply_markup=markup)

        elif message.text == 'Случайная История':
            NewURL = GetCategories(URL, 1)
            print('NewURL ', NewURL)

            if FirstVisitStories == True:
                list_of_stories = parser(NewURL)
                random.shuffle(list_of_stories)
                FirstVisitStories = False

            if len(list_of_stories) < 1:
                list_of_jokes = parser(NewURL)
                random.shuffle(list_of_jokes)

            if len(list_of_stories[0]) > 4096:
                for i in range(0, len(list_of_stories[0]), 4096):
                    bot.send_message(message.chat.id, list_of_stories[0][i:i + 4096])
            else:
                bot.send_message(message.chat.id, list_of_stories[0])

            del list_of_stories[0]

        elif message.text == 'Фраза':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('Случайная Фраза')
            item2 = types.KeyboardButton('Назад')
            markup.add(item1, item2)

            bot.send_message(message.chat.id, 'Фраза', reply_markup=markup)

        elif message.text == 'Случайная Фраза':
            NewURL = GetCategories(URL, 2)
            print('NewURL ', NewURL)

            if FirstVisitAphorisms == True:
                list_of_aphorisms = parser(NewURL)
                random.shuffle(list_of_aphorisms)
                FirstVisitAphorisms = False

            if len(list_of_aphorisms) < 1:
                list_of_aphorisms = parser(NewURL)
                random.shuffle(list_of_aphorisms)

            bot.send_message(message.chat.id, list_of_aphorisms[0])

            del list_of_aphorisms[0]

        elif message.text == 'Стих':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('Случайный Стих')
            item2 = types.KeyboardButton('Назад')
            markup.add(item1, item2)

            bot.send_message(message.chat.id, 'Стих', reply_markup=markup)

        elif message.text == 'Случайный Стих':
            NewURL = GetCategories(URL, 3)
            print('NewURL ', NewURL)

            if FirstVisitPoems == True:
                list_of_poems = parser(NewURL)
                random.shuffle(list_of_poems)
                FirstVisitPoems = False

            if len(list_of_poems) < 1:
                list_of_poems = parser(NewURL)
                random.shuffle(list_of_poems)

            bot.send_message(message.chat.id, list_of_poems[0])
            del list_of_poems[0]

        elif message.text == 'Информация о боте':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('Назад')
            markup.add(item1)

            bot_info = 'Здравствуй, пользователь! Этого бота создал студент группы М7О-406С-19 Алексин Антон.\n' \
                       'Как он работает?\n' \
                       'Производится парсинг сайта anekdot.ru, а именно нескольких категорий, таких как:\n' \
                       'Анекдоты, Истории, Фразы, Стишки.\n' \
                       'При нажатии на соответствующую клавишу на выплывающей клавиатуре ' \
                       'вы попадёте в подменю, в котором сможете вызывать элементы соответствующей ' \
                       'категории.'
            bot.send_message(message.chat.id, bot_info, reply_markup=markup)

        elif message.text == 'Назад':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('Анекдот')
            item2 = types.KeyboardButton('История')
            item3 = types.KeyboardButton('Фраза')
            item4 = types.KeyboardButton('Стих')
            item5 = types.KeyboardButton('Информация о боте')
            markup.add(item1, item2, item3, item4, item5)

            bot.send_message(message.chat.id, 'Здравствуйте! Вас приветствует бот шуток!', reply_markup=markup)

# Позволяет боту постоянно следить за сообщениями от пользователей
bot.polling()
