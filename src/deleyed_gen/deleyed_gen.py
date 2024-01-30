# -*- coding: utf-8 -*-
import requests
import json
from time import sleep
from deleyed_gen.env import api_key, url_store, url_delivery, url_orders, url_sales, url_paid_storage_create, url_paid_storage_download, url_paid_storage_status
# from env import api_key, url_store, url_delivery, url_orders, url_sales, url_paid_storage_create, url_paid_storage_download, url_paid_storage_status

class statistics:

    def __init__(self, params):
        self.status_error = 0
        self.header = {
                        "Authorization" : api_key
                        }
        self.param = params

    def get_params(self, url : str):
        self.respon = requests.get(url, headers=self.header, params=self.param)
        if self.respon.status_code == 200 :
            resp_dict = self.respon.json()
            return [resp_dict, self.respon.status_code]
        else :
            self.status_error = self.respon.status_code
            return ["error", self.respon.status_code]

    def get_repons(self, url : str):
        self.respon = requests.get(url, headers=self.header, json=self.param)
        if self.respon.status_code == 200 :
            resp_dict = self.respon.json()
            return resp_dict 
        else :
            self.status_error = self.respon.status_code
            return self.respon.status_code
        
    def post_request(self, url : str):
        self.request = requests.post(url, headers=self.header, json=self.param)
        if self.request.status_code == 201:
            req_dict = self.request.json()
            return [201, req_dict]
        else :
            self.status_error = self.request.status_code
            return [self.request.status_code, "error"] # сделать обработчик ошибок


class deliveries_and_store(statistics):

    def __init__(self, dateFrom):
        self.glist = []
        params = {
                        "dateFrom" : dateFrom
                        }
        statistics.__init__(self, params)
        
    def get_deliveries(self):
        return self.get_repons(url_delivery)
        
    def get_store(self):
        request_data = self.get_params(url_store)
        if request_data[1] == 200:
            with open("store.json", "w") as write_file:
                json.dump(request_data, write_file, indent=4)
            tmp_list = ["lastChangeDate", "warehouseName", "supplierArticle", "nmId", "barcode", 
                    "quantity", "inWayToClient", "inWayFromClient", "quantityFull", "category",
                    "subject", "brand", "techSize", "Price", "Discount", "isSupply", "isRealization", 
                    "SCCode"]
            self.glist.append(tmp_list)
            for data in request_data[0]:
                tmp_list = list(data.values())
                self.glist.append(tmp_list)
        # return self.get_repons(url_store)


class orders_and_slaes(statistics):

    def __init__(self, dateFrom, flag = 1):
        self.glist = []
        
        params = {
                    "dateFrom" : dateFrom,
                    "flag" : flag
                    }
        statistics.__init__(self, params)

    def get_orders(self):
        self.request_data = self.get_params(url_orders)
        if self.request_data[1] == 200:
            with open("orders.json", "w") as write_file:
                json.dump(self.request_data, write_file, indent=4)
        # for data in self.request_data[0]:
        #         if data["orderType"] == "Клиентский":
        #             tmp_list = list(data.values())
        #             self.glist.append(tmp_list)
        # return self.respon(url_orders)
    
    def get_sales(self):
        return self.respon(url_sales)

    
class paid_storage(statistics):

    def __init__(self, dateFrom, dateTo, diviser = 1, remainder = 0):
        self.glist = []
        params = {
                    "type": "paid_storage",
                    "params": {
                        "dateFrom": dateFrom,
                        "dateTo": dateTo,
                        "diviser": diviser,
                        "remainder": remainder
                    }
                    }
        statistics.__init__(self, params)

    def _respons_status(self):
        result = self.get_repons(url_paid_storage_status)
        status = result['data']['tasks'][0]['status'] 
        if status == 'done':
            self._status = 0
            return 0
        elif status == 'purged' or status == 'canceled':
            self._status = 1
            return 1
        else:
            return 2

    def get_paid_storage(self):
        request_id = self.post_request(url_paid_storage_create)
        sleep(60)
        if request_id[0] != 201:
            return request_id
        self.param = {
                        "ids": [request_id[1]['data']['taskId']]
                    }
        while (self._respons_status() == 2):
            sleep(60)
        if self._status == 1:
            self.status_error = 501
            return 501
        self.param = {
                        "id": request_id[1]['data']['taskId']
                        }
        request_data = self.get_repons(url_paid_storage_download)
        with open("paid_storage.json", "w") as write_file:
            json.dump(request_data, write_file, indent=4)

        tmp_list = ["date", "logWarehouseCoef", "officeId", "warehouse", "warehouseCoef", 
                    "giId", "chrtId", "size", "barcode", "subject", "brand", "vendorCode",
                    "nmId", "volume", "calcType", "warehousePrice", "barcodesCount", 
                    "palletPlaceCode", "palletCount"]
        self.glist.append(tmp_list)
        for data in request_data:
            tmp_list = list(data.values())
            self.glist.append(tmp_list)

# test = orders_and_slaes("2024-01-23")
# test.get_orders()
# print(test.glist)