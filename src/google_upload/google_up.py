import gspread
import json
from google_upload.env import service_acc

class google_api():

    def __init__(self):
        self.gc = gspread.service_account(filename=service_acc)
    
    def _open_doc(self, name_doc : str):
        self.sh = self.gc.open(name_doc)

    def _open_work_sheet(self, name_worksheet : str):
        self.worksheet_list = self.sh.worksheet(name_worksheet)

    def _create_work_sheet(self, name_worksheet : str):
        self.worksheet_list = self.sh.add_worksheet(title=name_worksheet, rows=1000, cols=40)

    def _upload_in_worksheet(self, glist : list):
        self.worksheet_list.insert_rows(glist)


        
