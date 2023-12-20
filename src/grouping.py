import json

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
        group = sorted_mas[0][0]
        # max_size_in_korob : int = max_kolvo[group]
        max_size_in_korob : int = 10
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
                # sorted_mas.pop(item)
    item = 1
    for i in ret_mas:
        print("korob",item, "---" ,i)
        item+=1

        


