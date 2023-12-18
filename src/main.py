import telebot
import parser_1
import sort
import grouping
from telebot import types
bot = telebot.TeleBot('6809416938:AAE-zQsdUhSdxgSyACYxPxCc620YzonYQ-U')

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    btn1 = types.KeyboardButton("Добавить отгрузку")
    btn2 = types.KeyboardButton("Разбить")
    btn3 = types.KeyboardButton("Как работает")
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, text="Привет, {0.first_name}! Я тестовый бот для добавления списка товаров в файлотгрузки!".format(message.from_user))
    

@bot.message_handler(content_types=['text'])
def get_text_messages(message): 
    if message.text == "Как работает":
        bot.send_message(message.from_user.id, "этот бот должен будет конвертировать текст в файл отгрузки (хз пока какой текст или мб даже файл будем грузить)")
    elif message.text == "Добавить отгрузку":
        bot.send_message(message.from_user.id, "в разроботке")
    elif message.text == "Разбить":
        bot.send_message(message.from_user.id, "в разроботке")
    else:
        bot.send_message(message.from_user.id, "ме")
        data = message.text
        parser_1.add_in_file(data)
        sorted_mas = sort.sorting()
        grouping.grouping(sorted_mas)


bot.polling(none_stop=True, interval=0)