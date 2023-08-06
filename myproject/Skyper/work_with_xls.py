import os
import re
from typing import List
import xlrd
import shutil
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_PATH = os.path.join(BASE_DIR, 'Documents/')

class FileProcessor:
    def __init__(
            self, files: List[str],
            sales_invoice='Видаткова накладна',
            score = 'Рахунок'
    ):
        self._files = files
        self._expense_invoices = []
        self._accounts = []
        self._sales_invoice = sales_invoice
        self._score = score

    def process_files(self):
        for file in os.listdir(BASE_PATH):
            if file.endswith(".xls") and os.path.getsize(BASE_PATH + file) > 0:
                if self._sales_invoice in file:
                    try:
                        self._expense_invoices.append(ExpenseInvoice(file))
                    except Exception as e:
                        logger.error(f"In process_files {self._sales_invoice}: {e}")

                elif self._score in file:
                    try:
                        self._accounts.append(Account(file))
                    except Exception as e:
                        logger.error(f"In process_files {self._score}: {e}")



class Invoice:
    _CLIENTS_FOLDER = BASE_PATH + 'clients/'
    _CLEANER_WORD = r'[^Ііа-яА-Яa-zA-Z\s]'

    def __init__(self, filename: str, number_and_date_cell: tuple, client_name_cell: tuple):
        self._filename = filename
        self._workbook = xlrd.open_workbook(BASE_PATH + filename)
        self._number_and_date_cell = number_and_date_cell
        self._client_name_cell = client_name_cell
        self._process()

    def _process(self):
        self._parse_invoice()

    def _parse_invoice(self):
        try:
            sheet = self._workbook.sheet_by_index(0)
            number_and_date = sheet.cell_value(*self._number_and_date_cell)
            client_name = sheet.cell_value(*self._client_name_cell)
            self._client_name = self._clean_client_name(client_name)

            logger.info(f"Filename: {self._filename}")
            logger.info(f"Number and date: {number_and_date}")
            logger.info(f"Client name: {self._client_name}")

            self._move_file_to_client_folder(self._client_name)
        except Exception as e:
            logger.error(f"In _parse_invoice: {e}")

    @staticmethod
    def _clean_client_name(client_name: str) -> str:
        try:
            return re.sub(Invoice._CLEANER_WORD, '', client_name)
        except Exception as e:
            logger.error(f"In _clean_client_name: {e}")

    def _move_file_to_client_folder(self, client_name: str):
        try:
            client_folder = os.path.join(self._CLIENTS_FOLDER, client_name)

            if not os.path.exists(client_folder):
                os.makedirs(client_folder)

            shutil.move(os.path.join(BASE_PATH, self._filename),
                        os.path.join(client_folder, os.path.basename(self._filename)))
        except Exception as e:
            logger.error(f"Error in _move_file_to_client_folder: {e}")


class ExpenseInvoice(Invoice):
    DATA_AND_NOMBER = (2, 1)
    CLIENT_NAME = (7, 6)

    def __init__(self, filename: str):
        super().__init__(filename, self.DATA_AND_NOMBER, self.CLIENT_NAME)

class Account(Invoice):
    DATA_AND_NOMBER = (15, 2)
    CLIENT_NAME = (20, 11)

    def __init__(self, filename: str):
        super().__init__(filename, self.DATA_AND_NOMBER, self.CLIENT_NAME)

def get_files(path: str) -> List[str]:
    files = []
    with os.scandir(path) as entries:
        for entry in entries:
            if entry.is_file() and entry.name.endswith('.xls'):
                files.append(entry.name)
    return files


def main():
    # parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    files = get_files(BASE_PATH)
    file_processor = FileProcessor(files)
    file_processor.process_files()

def run_main_loop():
    while True:
        main()

if __name__ == '__main__':
    main()
