from deleyed_gen.deleyed_gen import paid_storage, deliveries_and_store
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
calendar_1_to = CallbackData('calendar_1_to', 'action', 'year', 'month', 'day')
calendar_2_from = CallbackData('calendar_2_from', 'action', 'year', 'month', 'day')
calendar_3_order = CallbackData('calendar_3_order', 'action', 'year', 'month', 'day')

now = datetime.datetime.now()
dataTo = ""
dataFrom = ""

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Добавить отгрузку")
    btn_deleyed_gen = types.KeyboardButton("Получить отчет о хранении")
    btn_get_stocks = types.KeyboardButton("Получить отчет по остаткам")
    btn_get_sales = types.KeyboardButton("Получить отчет по продажам за день")
    markup.add(btn1, btn_deleyed_gen, btn_get_stocks, btn_get_sales )
    bot.send_message(message.chat.id, text="Привет, {0.first_name}! Используй кнопки".format(message.from_user), reply_markup=markup)

@bot.message_handler(content_types=['text'])
def get_text_messages(message): 
    if message.text == "Добавить отгрузку":
        bot.send_message(message.from_user.id, "Введите навзание отгрузки, которое будет отображаться в названии листа googlesheet")
        bot.register_next_step_handler(message, get_name_worksheet)
    elif message.text == "Получить отчет о хранении":
        bot.send_message(message.from_user.id, 
                         "Выберете дату начала отчета", 
                         reply_markup=calendar.create_calendar(
                                                                name=calendar_2_from.prefix,
                                                                year=now.year,
                                                                month=now.month),
                        )
    elif message.text == "Получить отчет по остаткам":
        bot.send_message(message.from_user.id, "Обработка началась")
        request_store_ = deliveries_and_store(now.strftime('%Y-%m-%d'))
        request_store_.get_store()
        g_push = google_api()
        g_push._open_doc("store_data")
        g_push._create_work_sheet(now.strftime("%d-%m-%Y(%H-%M)"))
        g_push._upload_in_worksheet(request_store_.glist)
        bot.send_message(message.from_user.id, "Обработка завершилась (смотри последний лист) https://docs.google.com/spreadsheets/d/1tYF3V-b0D1AfPg7QVObwZ3T1eaPbsMpS9WBoRak0oDk/edit?usp=sharing")
    elif message.text == "Получить отчет по продажам":
        bot.send_message(message.from_user.id, "Обработка началась")

        bot.send_message(message.from_user.id, "Кнопки")
    else:
        bot.send_message(message.from_user.id, "ме")
        

@bot.callback_query_handler(func=lambda call: call.data.startswith(calendar_1_to.prefix))  #  
def callback_inline(call: CallbackQuery):
    """
    Обработка inline callback запросов
    :param call:
    :return:
    """

    # At this point, we are sure that this calendar is ours. So we cut the line by the separator of our calendar
    name, action, year, month, day = call.data.split(calendar_1_to.sep)
    # Processing the calendar. Get either the date or None if the buttons are of a different type
    date = calendar.calendar_query_handler(
        bot=bot, call=call, name=name, action=action, year=year, month=month, day=day
    )
    # There are additional steps. Let's say if the date DAY is selected, you can execute your code. I sent a message.
    if action == "DAY":
        bot.send_message(
            chat_id=call.from_user.id,
            text=f"По {date.strftime('%Y-%m-%d')}",
            reply_markup=ReplyKeyboardRemove(),
        )
        dataTo = date.strftime('%Y-%m-%d')
        bot.send_message(chat_id=call.from_user.id,
                         text="Обработка началась")
        request_paid_storage = paid_storage(dataFrom, dataTo)
        request_paid_storage.get_paid_storage()
        g_push = google_api()
        g_push._open_doc("paid_storage")
        g_push._create_work_sheet(dataFrom + "-" + dataTo + "-" + now.strftime("%d-%m-%Y(%H-%M)"))
        g_push._upload_in_worksheet(request_paid_storage.glist)
        bot.send_message(chat_id=call.from_user.id,
                         text="Обработка завершилась. Новый документ лежит тут https://docs.google.com/spreadsheets/d/1EPFRm7DEhWbFKmWhcRIXnuYG8LqVbnpZEN9dq-hcWgU/edit?usp=sharing (смотри по текущей дате и времени)")
    elif action == "CANCEL":
        bot.send_message(
            chat_id=call.from_user.id,
            text="Cancellation",
            reply_markup=ReplyKeyboardRemove(),
        )
        print(f"{calendar_1_to}: Cancellation")

@bot.callback_query_handler(func=lambda call: call.data.startswith(calendar_2_from.prefix))  #  
def callback_inline(call: CallbackQuery):
    """
    Обработка inline callback запросов
    :param call:
    :return:
    """

    # At this point, we are sure that this calendar is ours. So we cut the line by the separator of our calendar
    name, action, year, month, day = call.data.split(calendar_2_from.sep)
    # Processing the calendar. Get either the date or None if the buttons are of a different type
    date = calendar.calendar_query_handler(
        bot=bot, call=call, name=name, action=action, year=year, month=month, day=day
    )
    # There are additional steps. Let's say if the date DAY is selected, you can execute your code. I sent a message.
    if action == "DAY":
        bot.send_message(
            chat_id=call.from_user.id,
            text=f"С {date.strftime('%Y-%m-%d')}",
            reply_markup=ReplyKeyboardRemove(),
        )
        global dataFrom
        dataFrom = date.strftime('%Y-%m-%d')
        bot.send_message(call.from_user.id, 
                         "Выберете дату конца отчета", 
                         reply_markup=calendar.create_calendar(
                                                                name=calendar_1_to.prefix,
                                                                year=now.year,
                                                                month=now.month)
                        )
        print("dataFrom -", dataFrom)
    elif action == "CANCEL":
        bot.send_message(
            chat_id=call.from_user.id,
            text="Cancellation",
            reply_markup=ReplyKeyboardRemove(),
        )
        print(f"{calendar_2_from}: Cancellation")

@bot.callback_query_handler(func=lambda call: call.data.startswith(calendar_3_order.prefix))  #  
def callback_inline(call: CallbackQuery):
    """
    Обработка inline callback запросов
    :param call:
    :return:
    """

    # At this point, we are sure that this calendar is ours. So we cut the line by the separator of our calendar
    name, action, year, month, day = call.data.split(calendar_3_order.sep)
    # Processing the calendar. Get either the date or None if the buttons are of a different type
    date = calendar.calendar_query_handler(
        bot=bot, call=call, name=name, action=action, year=year, month=month, day=day
    )
    # There are additional steps. Let's say if the date DAY is selected, you can execute your code. I sent a message.
    if action == "DAY":
        bot.send_message(
            chat_id=call.from_user.id,
            text=f"Дата {date.strftime('%Y-%m-%d')}",
            reply_markup=ReplyKeyboardRemove(),
        )
        
    elif action == "CANCEL":
        bot.send_message(
            chat_id=call.from_user.id,
            text="Cancellation",
            reply_markup=ReplyKeyboardRemove(),
        )
        print(f"{calendar_1_to}: Cancellation")

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

def gett_paid_storage(message):
    bot.send_message(message.from_user.id, text=f"С {dataFrom} по {dataTo}")
    print(dataFrom, dataTo)


name_worksheet : str = None
bot.polling(none_stop=True, interval=0)