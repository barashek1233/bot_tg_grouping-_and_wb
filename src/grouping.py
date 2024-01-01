import json
from data import formula_art, formula_razmera

def grouping(sorted_mas : list):
    ret_mas = []
    with open("data_file.json", "r") as read_file:
        r_file : dict = json.load(read_file)
    with open("group_kolvo.json", "r") as ma_kolvo:
        max_kolvo : dict = json.load(ma_kolvo)
    item = 0
    len_mas = len(sorted_mas)
    # while sorted_mas:
    while len_mas > item:
        group = sorted_mas[item][0]
        # print("group ", group)
        max_size_in_korob : int = max_kolvo[group]
        # print("max_size", max_size_in_korob)
        # max_size_in_korob : int = 10
        tmp_korob : list = []
        while max_size_in_korob > 0 and len_mas > item:
            if r_file[sorted_mas[item][2]]['kol-vo'] == max_size_in_korob:
                tmp_korob.append(sorted_mas[item][2])  # in func or class
                tmp_korob.append(max_size_in_korob)
                max_size_in_korob = 0
                ret_mas.append(tmp_korob)
                # sorted_mas.pop(item)
                item += 1
                break

            elif r_file[sorted_mas[item][2]]['kol-vo'] > max_size_in_korob:
                tmp_korob.append(sorted_mas[item][2])
                tmp_korob.append(max_size_in_korob)
                ret_mas.append(tmp_korob)
                r_file[sorted_mas[item][2]]['kol-vo'] = r_file[sorted_mas[item][2]]['kol-vo'] - max_size_in_korob
                max_size_in_korob = 0
                break

            elif r_file[sorted_mas[item][2]]['kol-vo'] < max_size_in_korob:
                tmp_korob.append(sorted_mas[item][2])
                tmp_korob.append(r_file[sorted_mas[item][2]]['kol-vo'])
                max_size_in_korob = max_size_in_korob - r_file[sorted_mas[item][2]]['kol-vo']
                item += 1
                if item < len_mas:
                    if group != sorted_mas[item+1][0]:
                        break
                # sorted_mas.pop(item)
    return ret_mas

        

def pred_up_in_boxes(mas : list):
    glist : list = []
    number_boxes : int = 0
    for box in mas:
        number_boxes += 1
        iter : int = 0
        index : int = 0
        while iter < len(box)/2:
            tmp_glist : list = []
            if iter == 0:
                tmp_glist.append(number_boxes)
            else:
                tmp_glist.append(" ")
            tmp_glist.append(formula_art)
            tmp_glist.append(box[index])
            tmp_glist.append(formula_razmera)
            index += 1
            tmp_glist.append(box[index])
            glist.append(tmp_glist)
            index += 1
            iter += 1
    return glist