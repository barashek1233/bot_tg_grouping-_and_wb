import gspread
import json
from google_upload.env import service_acc

class google_api():

    def __init__(self):
        self.gc = gspread.service_account(filename=service_acc)
        # self.gc = gspread.service_account(filename="/app/grouping_goods_into_boxes/src/google_upload/service_account.json")
    
    def _open_doc(self, name_doc : str):
        self.sh = self.gc.open(name_doc)

    def _open_work_sheet(self, name_worksheet : str):
        self.worksheet_list = self.sh.worksheet(name_worksheet)

    def _create_work_sheet(self, name_worksheet : str):
        self.worksheet_list = self.sh.add_worksheet(title=name_worksheet, rows=1000, cols=40)

    def _upload_in_worksheet(self, glist : list):
        self.worksheet_list.insert_rows(glist)

    def _update_in_worksheet(self, rang, glist):
        self.worksheet_list.update(rang, glist)

    def _get_all_values(self):
        """Returns a list of lists containing all cells' values as strings."""
        return self.worksheet_list.get_all_values()
        
