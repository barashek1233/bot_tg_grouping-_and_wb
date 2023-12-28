import gspread
# Указываем путь к JSON
gc = gspread.service_account(filename='mypython-408913-267a81584536.json')
#Открываем тестовую таблицу
sh = gc.open("Копия Отгрузки-2")
#Выводим значение ячейки A1
worksheet_list = sh.worksheets()
print(worksheet_list)