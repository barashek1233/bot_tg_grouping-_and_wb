from deleyed_gen.deleyed_gen import orders_and_slaes 

def get_order(data):
    test = orders_and_slaes(data)
    test.get_orders()
    for data in test.request_data[0]:
        if data["orderType"] == "Клиентский":
            tmp_list = list(data.values())
            test.glist.append(tmp_list)
    return test.glist
        

# glist = get_order("2024-01-23")
# # for item in glist:
# #     print(item)
# for data in glist:
#     if data["orderType"] == "Клиентский":
#         print(data)