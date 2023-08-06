import os
import re
from typing import List
import xlrd
import shutil
import logging
from datetime import datetime

from .config import BASE_PATH,  CLIENTS_FOLDER
from .config import FILE_NAME_1, FILE_NAME_2
from .config import ACCOUNT_DATA_AND_NOMBER, ACCOUNT_CLIENT_NAME
from .config import INVOICE_DATA_AND_NOMBER, INVOICE_CLIENT_NAME


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class InvoiceDetailsExtractor:
    pass

class FileProcessor:
    def __init__(
            self, files: List[str],
            sales_invoice=FILE_NAME_1,
            score = FILE_NAME_2
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

    @staticmethod
    def get_files(path: str) -> List[str]:
        files = []
        with os.scandir(path) as entries:
            for entry in entries:
                if entry.is_file() and entry.name.endswith('.xls'):
                    files.append(entry.name)
        return files

class Invoice:
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
            client_folder = os.path.join(CLIENTS_FOLDER, client_name)

            if not os.path.exists(client_folder):
                os.makedirs(client_folder)

            shutil.move(os.path.join(BASE_PATH, self._filename),
                        os.path.join(client_folder, os.path.basename(self._filename)))
        except Exception as e:
            logger.error(f"Error in _move_file_to_client_folder: {e}")

class ExpenseInvoice(Invoice):
    def __init__(self, filename: str):
        super().__init__(filename, INVOICE_DATA_AND_NOMBER, INVOICE_CLIENT_NAME)

class Account(Invoice):
    def __init__(self, filename: str):
        super().__init__(filename, ACCOUNT_DATA_AND_NOMBER, ACCOUNT_CLIENT_NAME)

class DateAndNumberExtractor(InvoiceDetailsExtractor):
    def __init__(self, input_string):
        self._input_string = input_string
        self._parsed_data = self._parsing_file()
        super().__init__()

    def _parsing_file(self):
        number_pattern = r'№ (\d+)'
        date_pattern = r'(\d{1,2}) (\w+) (\d{4})'

        number = re.search(number_pattern, self._input_string).group(1)
        day, month_name, year = re.search(date_pattern, self._input_string).groups()

        return [number, day, month_name, year]

    @staticmethod
    def _date_formating(*date_data):
        months_ua = {
            "січня": "01", "лютого": "02", "березня": "03", "квітня": "04", "травня": "05", "червня": "06",
            "липня": "07", "серпня": "08", "вересня": "09", "жовтня": "10", "листопада": "11", "грудня": "12"
        }

        day, month_name, year = date_data[1], date_data[2], date_data[3]
        month_number = months_ua.get(month_name.lower())
        date_str = f"{day}.{month_number}.{year}"
        date_obj = datetime.strptime(date_str, "%d.%m.%Y").date()
        return [date_str, date_obj, date_data[0]]

    def date_in_str(self):
        result = self._date_formating(*self._parsed_data)
        return result[0]

    def date_in_datefield(self):
        result = self._date_formating(*self._parsed_data)
        return result[1]

    def number_invoice(self):
        result = self._date_formating(*self._parsed_data)
        return result[2]

def run_work_loop():
    while True:
        files = FileProcessor.get_files(BASE_PATH)
        file_processor = FileProcessor(files)
        file_processor.process_files()


