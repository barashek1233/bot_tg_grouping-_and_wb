from deleyed_gen.deleyed_gen import deliveries_and_store
from google_upload.google_up import google_api
import datetime


class store():

    def __init__(self):
        self.request_store = deliveries_and_store("2023-01-01")
        self.request_store.get_store()
        if __name__ == "__main__":
            g_push = google_api()
            g_push._open_doc("store_data")
            g_push._create_work_sheet("test2")
            g_push._upload_in_worksheet(self.request_store.glist)
        


    def grouping(self):
        self.grouping_store_data = {}
        for line in self.request_store.request_data[0]:
            if line['nmId'] in self.grouping_store_data:
                self.grouping_store_data[line['nmId']][1] = self.grouping_store_data[line['nmId']][1] + line['inWayToClient']
                self.grouping_store_data[line['nmId']][2] = self.grouping_store_data[line['nmId']][2] + line['inWayFromClient']
                self.grouping_store_data[line['nmId']][0] = self.grouping_store_data[line['nmId']][0] + line['quantity']
            else:
                self.grouping_store_data[line['nmId']] = [line['inWayToClient'], line['inWayFromClient'], line['quantity']]

        
    def dict_to_list(self):
        self.glist = []
        self.glist.append(["Артикул WB", "В пути до клиента", "В пути от клиента", "Итого по складам"])
        for key in self.grouping_store_data:
            tmp_glist = [key, str(self.grouping_store_data[key][0]), str(self.grouping_store_data[key][1]), str(self.grouping_store_data[key][2])]
            self.glist.append(tmp_glist)
        print(self.glist)

if __name__ == "__main__":
    # now.strftime('%Y-%m-%d')
    test = store()
    # test.grouping()
    # test.dict_to_list()
    # print(test.glist)
    # g_push = google_api()
    # g_push._open_doc("store_data")
    # g_push._create_work_sheet("test")
    # g_push._upload_in_worksheet(test.glist)