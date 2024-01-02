import telebot
import parser_1
import sort
import grouping
import up_google
from dataa import API_KEY
from telebot import types
bot = telebot.TeleBot(API_KEY)


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Добавить отгрузку")
    btn3 = types.KeyboardButton("Как работает")
    markup.add(btn1, btn3)
    bot.send_message(message.chat.id, text="Привет, {0.first_name}! Я тестовый бот для добавления списка товаров в файлотгрузки!".format(message.from_user), reply_markup=markup)

@bot.message_handler(content_types=['text'])
def get_text_messages(message): 
    if message.text == "Как работает":
        bot.send_message(message.from_user.id, "этот бот конвертирует текст в файл отгрузки в гугл документе, для его работы нажми кнопку добавить отгрузку и следуй инструкциям")
    elif message.text == "Добавить отгрузку":
        bot.send_message(message.from_user.id, "Введите навзание отгрузки, которое будет отображаться в названии листа гугл документа")

        bot.register_next_step_handler(message, get_name_worksheet)


    else:
        bot.send_message(message.from_user.id, "ме")
        

def get_name_worksheet(message):
    print("3")
    name_worksheet = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn4 = types.KeyboardButton("Да")
    btn5 = types.KeyboardButton("нет")
    markup.add(btn4, btn5)
    bot.send_message(message.from_user.id, "Все верно?",reply_markup=markup)
    bot.register_next_step_handler(message, check_na_oshib, name_worksheet)

def check_na_oshib(message, name_worksheet):
    if message.text == "Да":
        bot.send_message(message.from_user.id, "Введите текст отгрузки. Самый оптимальный вариант скопировать его из гугл таблиц. ВАЖНО!!!! текст должен быть формата (артикул размер баркод количество) без пробелов в артикуле или размере")
        bot.register_next_step_handler(message, otgruzka_poshla, name_worksheet)
    else:
        bot.send_message(message.from_user.id, "lox")

def otgruzka_poshla(message, name_worksheet):
    print("voshel")
    data = message.text
    parser_1.add_in_file(data)
    sorted_mas = sort.sorting()
    po_korobam : list = grouping.grouping(sorted_mas)
    glist : list = grouping.pred_up_in_boxes(po_korobam)
    # print(po_korobam)
    # upload_to_google(po_korobam, "otgruzka1")
    up_google.google_api(glist, name_worksheet)

name_worksheet : str = None
bot.polling(none_stop=True, interval=0)