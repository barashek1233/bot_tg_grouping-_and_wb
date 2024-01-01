import json
def add_in_file():
    with open("all_barcode_file.json", "r") as read_file:
        data = json.load(read_file)
    with open("test.json", "w") as write_in_file:
        json.dump(data, write_in_file, indent=4, ensure_ascii=True)

# add_in_file()

def main():
    with open("test.json", "r") as read_file:
        data = json.load(read_file)
    dicktionary = {}
    tmp_dicktionary = {}
    for i in range(len(data['result'])):
        tmp_mas = []
        tmp_mas.append(data['result'][i][2])
        tmp_mas.append(data['result'][i][3])
        tmp_mas.append(data['result'][i][4])
        # tmp_dicktionary['group'] = data['result'][i][2]
        # tmp_dicktionary['subgroup'] = data['result'][i][3]
        # tmp_dicktionary['kol-vo'] = data['result'][i][4]
        # print(tmp_dicktionary)
        dicktionary[data['result'][i][0]] = tmp_mas
    with open("rest.json", "w") as rest:
        json.dump(dicktionary, rest, indent=4)
    print(dicktionary)
    
if __name__ == __main__ :
    main()