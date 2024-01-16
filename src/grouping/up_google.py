import gspread

def add_boxes_in_table(worksheet_list, glist : list):
    cell_letter : str = 65
    cell_number : str = 1
    number_boxes : int = 0
    for box in glist:
        number_boxes += 1
        cell_letter : str = 65
        iter : int = 0  #  для итериции по строкам таблицы в одной коробке
        index : int = 0  #  для доступа к элементам коробки из массива
        cell : str = chr(cell_letter) + str(cell_number)  #  A
        worksheet_list.update(cell, number_boxes)
        while iter < len(box) / 2:
            cell_letter : str = 66

            cell_letter = cell_letter + 1  #  B
            cell = chr(cell_letter) + str(cell_number)
            worksheet_list.update(cell, box[index])
            index += 1

            cell_letter = cell_letter + 1  #  C
            cell = chr(cell_letter) + str(cell_number)
            worksheet_list.update(cell, "razmer")

            cell_letter = cell_letter + 1  #  D
            cell = chr(cell_letter) + str(cell_number)
            worksheet_list.update(cell, box[index])
            index += 1

            iter += 1
            cell_number += 1


def google_api(glist : list, name_worksheet : str):
    # Указываем путь к JSON
    gc = gspread.service_account(filename='grouping/mypython-408913-267a81584536.json')
    #Открываем тестовую таблицу
    sh = gc.open("Копия Отгрузки-2")
    worksheet_list = sh.add_worksheet(title=name_worksheet, rows=100, cols=20)
    # add_boxes_in_table(worksheet_list, glist)
    # worksheet_list.insert_rows(glist)
    worksheet_list.insert_rows(glist)
