import json

# def custom_key(group):
#     return group[1]
# key=custom_key

def sort(data):
    """
    sort(data)
    return sorted list
    """
    mas = []
    for i in data:
        tmp_mas = []
        tmp_mas.append(str(data[i]['group']))
        tmp_mas.append(str(data[i]['subgroup']))
        tmp_mas.append(str(i))
        mas.append(tmp_mas)
    mas.sort()
    # print(mas)
    return mas


def sorting():
    """
    main_func()
    return sorted list from data_file.json
    """
    with open("data_file.json", "r") as read_file:  # необходимо добавить проверку на корректность данных  данном файле
        data = json.load(read_file)
    return sort(data)
    
    

