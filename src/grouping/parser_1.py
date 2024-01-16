import json


def sopen_read_file():
    with open("grouping/rest.json", "r") as read_file:
        data = json.load(read_file)
    return data


def search_group_in_file(barcode, data):
    group = data[barcode][0]
    return group

def search_subgroup_in_file(barcode, data):
    return data[barcode][1]

def my_parser(data):
    dictionary = {}
    a = 1
    str = data.split("\n")
    read_file = sopen_read_file()

    for arg in str:
        dic = {}
        word = arg.split()
        if word[2] in dictionary:
            dictionary[word[2]]['kol-vo'] = dictionary[word[2]]['kol-vo'] + int(word[3])
        else:
            dic['group'] = search_group_in_file(word[2], read_file)
            dic['subgroup'] = search_subgroup_in_file(word[2], read_file)
            dic['kol-vo'] = int(word[3])
            dic['arg'] = word[0]
            dic['razmer'] = word[1]
            dictionary[word[2]] = dic

    return dictionary
    
def add_in_file(data):
    dictionary = my_parser(data)
    with open("data_file.json", "w") as write_file:
        json.dump(dictionary, write_file, indent=4, ensure_ascii=True)