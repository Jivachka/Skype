import os
import re
from typing import List
import xlrd
import shutil
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FileProcessor:
    BASE_PATH = 'Documents/'

    def __init__(self, files: List[str]):
        self.files = files
        self.expense_invoices = []
        self.accounts = []

    def process_files(self):
        for file in os.listdir(FileProcessor.BASE_PATH):
            if file.endswith(".xls") and os.path.getsize(FileProcessor.BASE_PATH + file) > 0:
                if 'Видаткова накладна' in file:
                    try:
                        self.expense_invoices.append(ExpenseInvoice(file))
                    except Exception as e:
                        logger.error(f"In process_files Видаткова накладна: {e}")

                elif 'Рахунок' in file:
                    try:
                        self.accounts.append(Account(file))
                    except Exception as e:
                        logger.error(f"In process_files Рахунок: {e}")


class Invoice:
    CLIENTS_FOLDER = 'Documents/clients/'
    CLEANER_WORD = r'[^Ііа-яА-Яa-zA-Z\s]'

    def __init__(self, filename: str, number_and_date_cell: tuple, client_name_cell: tuple):
        self.filename = filename
        self.workbook = xlrd.open_workbook(FileProcessor.BASE_PATH + filename)
        self.number_and_date_cell = number_and_date_cell
        self.client_name_cell = client_name_cell
        self.process()

    def process(self):
        self.parse_invoice()

    def parse_invoice(self):
        try:
            sheet = self.workbook.sheet_by_index(0)
            number_and_date = sheet.cell_value(*self.number_and_date_cell)
            client_name = sheet.cell_value(*self.client_name_cell)
            self.client_name = self.clean_client_name(client_name)

            logger.info(f"Filename: {self.filename}")
            logger.info(f"Number and date: {number_and_date}")
            logger.info(f"Client name: {self.client_name}")

            self.move_file_to_client_folder(self.client_name)
        except Exception as e:
            logger.error(f"In parse_invoice: {e}")


    @staticmethod
    def clean_client_name(client_name: str) -> str:
        try:
            return re.sub(Invoice.CLEANER_WORD, '', client_name)
        except Exception as e:
            logger.error(f"In clean_client_name: {e}")

    def move_file_to_client_folder(self, client_name: str):
        try:
            client_folder = os.path.join(self.CLIENTS_FOLDER, client_name)

            if not os.path.exists(client_folder):
                os.makedirs(client_folder)

            shutil.move(os.path.join(FileProcessor.BASE_PATH, self.filename),
                        os.path.join(client_folder, os.path.basename(self.filename)))
        except Exception as e:
            logger.error(f"In move_file_to_client_folder: {e}")

class ExpenseInvoice(Invoice):
    def __init__(self, filename: str):
        super().__init__(filename, (2, 1), (7, 6))


class Account(Invoice):
    def __init__(self, filename: str):
        super().__init__(filename, (15, 2), (20, 11))


def get_files(path: str) -> List[str]:
    files = []
    with os.scandir(path) as entries:
        for entry in entries:
            if entry.is_file() and entry.name.endswith('.xls'):
                files.append(entry.name)
    return files


def main():
    # parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path_to_files = 'Documents/'
    files = get_files(path_to_files)

    file_processor = FileProcessor(files)
    file_processor.process_files()

def run_main_loop():
    while True:
        main()

if __name__ == '__main__':
    main()
