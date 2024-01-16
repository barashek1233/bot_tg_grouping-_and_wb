import json
import gspread

def tmain():
    gc = gspread.service_account(filename='mypython-408913-267a815845.json')
    #Открываем тестовую таблицу
    sh = gc.open("dmin111")
    ws = sh.worksheet("Лист1")
    list_of_lists = ws.get_all_values()
    dicktionary = {}
    for id in list_of_lists:
        tmp_mas : list= []
        tmp_mas.append(int(id[1]))
        tmp_mas.append(int(id[2]))
        tmp_mas.append(int(id[3]))
        dicktionary[id[0]] = tmp_mas
    with open("../grouping/rest.json", "w") as write_file:
        json.dump(dicktionary, write_file, indent=4)


if __name__ == "__main__" :
    tmain()