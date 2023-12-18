import json

def grouping(sorted_mas):
    ret_mas = []
    with open("data_file.json", "r") as read_file:
        r_file = json.load(read_file)
    with open("group_kolvo.json", "r") as ma_kolvo:
        max_kolvo = json.load(ma_kolvo)
        # print(sorted_mas)
    for barcode in sorted_mas:
        subgroup = max_kolvo[barcode[0]]
        # print(barcode)
        if r_file[barcode[2]]['kol-vo'] > subgroup:
            
            tmp_mas = []
            tmp_mas.append(barcode[2])
            tmp_mas.append(r_file[barcode[2]]["kol-vo"])
            r_file[barcode[2]]["kol-vo"] = r_file[barcode[2]]["kol-vo"] - subgroup
            ret_mas.append(tmp_mas)
        elif r_file[barcode[2]]['kol-vo'] == subgroup:
            tmp_mas = []
            tmp_mas.append(barcode[2])
            tmp_mas.append(r_file[barcode[2]]["kol-vo"])
            tmp_mas.append("chotko_vlezlo")
            ret_mas.append(tmp_mas)
            del r_file[barcode[2]]
        elif r_file[barcode[2]]['kol-vo'] < subgroup:
            tmp_mas = []
            tmp_mas.append(barcode[2])
            tmp_mas.append(r_file[barcode[2]]["kol-vo"])
            tmp_mas.append("vlezet_eshcho")
            ret_mas.append(tmp_mas)
            del r_file[barcode[2]]
    for i in ret_mas:
        print(i)

