from deleyed_gen.deleyed_gen import paid_storage
import telebot
import grouping.parser_1 as parser_1
import grouping.sort as sort
import grouping.grouping as grouping
import grouping.up_google as up_google
from google_upload.google_up import google_api
from grouping.dataa import API_KEY

from telebot import types
from telebot.types import ReplyKeyboardRemove, CallbackQuery
import datetime
import telebot_calendar
from telebot_calendar import Calendar, RUSSIAN_LANGUAGE, CallbackData 

logger = telebot.logger
bot = telebot.TeleBot(API_KEY)

calendar = Calendar(language=RUSSIAN_LANGUAGE)
calendar_1 = CallbackData('calendar_1', 'action', 'year', 'month', 'day')

now = datetime.datetime.now()
data = ""

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Добавить отгрузку")
    btn_deleyed_gen = types.KeyboardButton("Получить отчет о хранении")
    markup.add(btn1, btn_deleyed_gen)
    bot.send_message(message.chat.id, text="Привет, {0.first_name}! Используй кнопки".format(message.from_user), reply_markup=markup)

@bot.message_handler(content_types=['text'])
def get_text_messages(message): 
    if message.text == "Добавить отгрузку":
        bot.send_message(message.from_user.id, "Введите навзание отгрузки, которое будет отображаться в названии листа googlesheet")
        bot.register_next_step_handler(message, get_name_worksheet)
    elif message.text == "Получить отчет о хранении":
        bot.send_message(message.from_user.id, 
                         "Выберете дату начала отчета (отчет будет сформирован по сегодняшний день)", 
                         reply_markup=calendar.create_calendar(
                                                                name=calendar_1.prefix,
                                                                year=now.year,
                                                                month=now.month)
                        )
    else:
        bot.send_message(message.from_user.id, "ме")
        

@bot.callback_query_handler(func=lambda call: call.data.startswith(calendar_1.prefix))
def callback_inline(call: CallbackQuery):
    """
    Обработка inline callback запросов
    :param call:
    :return:
    """

    # At this point, we are sure that this calendar is ours. So we cut the line by the separator of our calendar
    name, action, year, month, day = call.data.split(calendar_1.sep)
    # Processing the calendar. Get either the date or None if the buttons are of a different type
    datetime_now = datetime.datetime.now()  #  current_datetime.strftime("%d-%m-%Y(%H-%M)")
    dateTo = datetime_now.strftime('%Y-%m-%d')
    date = calendar.calendar_query_handler(
        bot=bot, call=call, name=name, action=action, year=year, month=month, day=day
    )
    dateFrom = date.strftime('%Y-%m-%d')
    # There are additional steps. Let's say if the date DAY is selected, you can execute your code. I sent a message.
    if action == "DAY":
        bot.send_message(
            chat_id=call.from_user.id,
            text=f"С {dateFrom} по {dateTo}",
            # reply_markup=ReplyKeyboardRemove(),
        )
        bot.send_message(chat_id=call.from_user.id,
                         text="Обработка началась")
        request_paid_storage = paid_storage(dateFrom, dateTo)
        request_paid_storage.get_paid_storage()
        g_push = google_api()
        g_push._open_doc("paid_storage")
        g_push._create_work_sheet(datetime_now.strftime("%d-%m-%Y(%H-%M)"))
        g_push._upload_in_worksheet(request_paid_storage.glist)
        bot.send_message(chat_id=call.from_user.id,
                         text="Обработка завершилась. Новый документ лежит тут https://docs.google.com/spreadsheets/d/1EPFRm7DEhWbFKmWhcRIXnuYG8LqVbnpZEN9dq-hcWgU/edit?usp=sharing (смотри по текущей дате и времени)")
        # print(f"{calendar_1}: Day: {date.strftime('%Y-%m-%d')}")
    elif action == "CANCEL":
        bot.send_message(
            chat_id=call.from_user.id,
            text="Cancellation",
            reply_markup=ReplyKeyboardRemove(),
        )
        print(f"{calendar_1}: Cancellation")

def get_name_worksheet(message):
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
    data = message.text
    parser_1.add_in_file(data)
    sorted_mas = sort.sorting()
    po_korobam : list = grouping.grouping(sorted_mas)
    glist : list = grouping.pred_up_in_boxes(po_korobam)
    up_google.google_api(glist, name_worksheet)
    bot.send_message(message.from_user.id, "Готово")

name_worksheet : str = None
bot.polling(none_stop=True, interval=0)