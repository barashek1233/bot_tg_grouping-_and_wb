from deleyed_gen.deleyed_gen import orders_and_slaes
from google_upload.google_up import google_api
import datetime

now = datetime.datetime.now()

class report_sales():

    def __init__(self):
        self.g_push = google_api()
        self.g_push._open_doc("Отчет по продажам")
        self.g_push._open_work_sheet("Заказы, шт")
        self.old_data_in_resport_sales = {}

    def counter_orders(self, date):
        rest = orders_and_slaes(date)
        rest.get_orders()
        date_time_obj = datetime.datetime.strptime(date, "%Y-%m-%d")
        self.supplier_article = {"data": date_time_obj.strftime("%d.%m")}
        
        for data in rest.request_data[0]:
            if data["orderType"] == "Клиентский":
                if data["supplierArticle"] in self.supplier_article:
                    self.supplier_article[data["supplierArticle"]] = self.supplier_article[data["supplierArticle"]] + 1
                else:
                    self.supplier_article[data["supplierArticle"]] = 1
        for key in self.supplier_article:
            count_sales_str = str(self.supplier_article[key])
            self.supplier_article[key] = count_sales_str

    def dict_to_list(self):
        glist :list = []
        for key in self.res:
            tmp_glist = []

            tmp_glist.append(key)
            for item in self.res[key]:
                tmp_glist.append(item)
            glist.append(tmp_glist)
        return glist

    def connecting_dictionar(self):
        for key in self.old_data_in_resport_sales:
            if key in self.supplier_article:
                self.old_data_in_resport_sales[key].insert(0, self.supplier_article[key])
                del self.supplier_article[key]
            else:
                self.old_data_in_resport_sales[key].insert(0, "0")

        for key in self.supplier_article:
            self.supplier_article[key] = [self.supplier_article[key]]
        
        self.res = self.old_data_in_resport_sales | self.supplier_article
        for key in self.res:
            if len(self.res[key]) > 15:
                self.res[key].pop()

    def get_old_values(self):
        old_data = self.g_push._get_all_values()
        for data in old_data:
            tmp_list=[]
            for index in range(1, len(data)):
                tmp_list.append(data[index])
            
        #     # if data[0] in self.dictionar:
            self.old_data_in_resport_sales[data[0]] = tmp_list

        # g_push._upload_in_worksheet(glist)
        # g_push._update_in_worksheet('A:B', glist)
    
    def push_in_ws(self, range, glist):
        self.g_push._update_in_worksheet(range, glist)


if __name__ == "__main__":
    
    test = report_sales()
    test.get_old_values()  #  old_data_in_resport_sales
    test.counter_orders("2024-01-27")
    test.connecting_dictionar()
    test.push_in_ws("A:Z", test.dict_to_list())

    #format 
    #
    # test.counter_orders("2024-01-24")
    # # test.connecting_dictionar()
    # test.push_in_ws("A:B", test.dict_to_list())
    pass


