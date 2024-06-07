import telebot
from telebot import types
import os

TOKEN = 'token'
bot = telebot.TeleBot(TOKEN)

BASE_DIR = 'content'
def create_markup(buttons):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for row in buttons:
        markup.row(*[types.KeyboardButton(button) for button in row])
    return markup

#List buttons
@bot.message_handler(commands=['start'])
def start(message):
    buttons = [['🇺🇦 Україна', '🇩🇪 Німечинна'],
               ['🇦🇹 Австрія', '🇨🇭 Швейцарія']]
    markup = create_markup(buttons)
    bot.send_message(message.chat.id,
                     f'Привіт, {message.from_user.first_name}! \nОбери країну, в якій ти зараз знаходишся ⬇',
                     reply_markup=markup)

#Dictionary country-cities
@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.chat.type == 'private':
        country_cities = {
            '🇺🇦 Україна': ['🇺🇦 Київ', '🇺🇦 Тернопіль'],
            '🇩🇪 Німечинна': ['🇩🇪 Мюнхен', '🇩🇪 Фюссен'],
            '🇦🇹 Австрія': ['🇦🇹 Зальцбург', '🇦🇹 Інсбрук'],
            '🇨🇭 Швейцарія': ['🇨🇭 Цюріх', '🇨🇭 Базель']
        }

        if message.text in country_cities:
            cities = country_cities[message.text]
            markup = create_markup([cities, ['⬅ Назад']])
            bot.send_message(message.chat.id, f'{message.from_user.first_name}, в якому ти місті ⬇',
                             reply_markup=markup)

        elif message.text == '⬅ Назад':
            buttons = [['🇺🇦 Україна', '🇩🇪 Німечинна'],
                       ['🇦🇹 Австрія', '🇨🇭 Швейцарія']]
            markup = create_markup(buttons)
            bot.send_message(message.chat.id,
                             f'Привіт, {message.from_user.first_name}! \nОбери країну, в якій ти зараз знаходишся ⬇',
                             reply_markup=markup)

        else:
            handle_city_selection(message.text, message)
def handle_city_selection(city, message):
    country_city_mapping = {
        '🇺🇦 Київ': ('Ukraine', 'Kyiv'),
        '🇺🇦 Тернопіль': ('Ukraine', 'Ternopil'),
        '🇩🇪 Мюнхен': ('Germany', 'Munich'),
        '🇩🇪 Фюссен': ('Germany', 'Fussen'),
        '🇦🇹 Зальцбург': ('Austria', 'Salzburg'),
        '🇦🇹 Інсбрук': ('Austria', 'Innsbruck'),
        '🇨🇭 Цюріх': ('Switzerland', 'Zurich'),
        '🇨🇭 Базель': ('Switzerland', 'Basel')
    }

    if city in country_city_mapping:
        country, city_name = country_city_mapping[city]
        city_dir = os.path.join(BASE_DIR, country, city_name)

        text_file = os.path.join(city_dir, 'text.txt')
        image_file = os.path.join(city_dir, 'jpeg.jpg')

        if os.path.exists(text_file):
            with open(text_file, 'r', encoding='utf-8') as file:
                text_content = file.read()
            bot.send_message(message.chat.id, text_content)

        if os.path.exists(image_file):
            with open(image_file, 'rb') as file:
                bot.send_photo(message.chat.id, file)

bot.polling(none_stop=True)