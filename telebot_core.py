# Импорт необходимых библиотек
import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import data_file

# Инициализация бота
TOKEN = '6025298232:AAGoesIM_VvWi5pjHXPEZC_-11CLpjZN9xA'
bot = telebot.TeleBot(TOKEN)


# Функция для создания клавиатуры с заданными кнопками и префиксом обратного вызова
def generate_keyboard(buttons, callback_prefix=""):
    keyboard = InlineKeyboardMarkup()
    for button_text in buttons:
        callback_data = callback_prefix + button_text
        keyboard.add(InlineKeyboardButton(button_text, callback_data=callback_data))
    return keyboard


# Функция для создания главной клавиатуры
def generate_main_keyboard():
    categories = data_file.main_dict.keys()
    keyboard = generate_keyboard(categories, callback_prefix="1")
    keyboard.add(InlineKeyboardButton("Таблица со всеми Промокодами!",
                                      url="https://docs.google.com/spreadsheets/d/1FhYGE5IODqbtXSfQGBs0BGUaUJYAWBGAC2SRWqYzf6M"))
    return keyboard


# Функция для создания второстепенной клавиатуры
def generate_secondary_keyboard(category):
    markets = data_file.main_dict[category]
    keyboard = generate_keyboard(markets, callback_prefix="2")
    keyboard.add(InlineKeyboardButton("В меню", callback_data="bm"))
    return keyboard


# Функция для создания клавиатуры "назад"
def generate_back_keyboard(market):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("В меню", callback_data="bm"))
    for category, markets in data_file.main_dict.items():
        if market in markets:
            keyboard.add(InlineKeyboardButton(category, callback_data="1" + category))
    return keyboard


# Обработчик текстовых сообщений
@bot.message_handler(content_types=['text'])
def handle_text_message(message):
    if message.text == '/start':
        bot.send_message(message.chat.id, "Выберите категорию в которой хотите получить скидку ⬇",
                         reply_markup=generate_main_keyboard())
    elif message.text in ['/stat_cat', '/stat_markets']:
        stat_dict = data_file.stat_cat_dict if message.text == '/stat_cat' else data_file.stat_markets_dict
        bot.send_message(message.chat.id, f"Статистика посещений {message.text[5:]}:")
        for k, v in stat_dict.items():
            bot.send_message(message.chat.id, f"{k}: {len(set(v))}")


# Обработчик обратных вызовов
@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    bot.answer_callback_query(callback_query_id=call.id)
    data = call.data[1:]
    flag = call.data[0]

    if flag == "1":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Выбирайте 🥰",
                              reply_markup=generate_secondary_keyboard(data))
        data_file.stat_cat_dict[data].append(call.from_user.id)
    elif flag == "2":
        bot.send_message(call.message.chat.id,
                         "Чтобы воспользоваться акцией необходимо: перейти по ссылке или скопировать промокод и ввести его на сайте или приложении магазина")
        data_file.stat_markets_dict[data].append(call.from_user.id)
        for text in data_file.text_dict[data]:
            bot.send_message(call.message.chat.id, text)
        bot.send_message(call.message.chat.id, "Куда отправимся за скидками дальше?",
                         reply_markup=generate_back_keyboard(data))
    elif flag == "b" and data == "m":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Выберите категорию в которой хотите получить скидку ⬇",
                              reply_markup=generate_main_keyboard())


print("Ready")
bot.infinity_polling()
