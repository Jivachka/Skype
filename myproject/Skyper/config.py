import os

# путь проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_PATH = os.path.join(BASE_DIR, 'Documents/')

# Названия типов документов
FILE_NAME_1 = 'Видаткова накладна'
FILE_NAME_2 = 'Рахунок'

CLIENTS_FOLDER = BASE_PATH + 'clients/'

# Позиции данных ячейки в екселе  для накладной
INVOICE_DATA_AND_NOMBER = (2, 1)
INVOICE_CLIENT_NAME = (7, 6)

# Позиции данных ячейки в екселе  для счета
ACCOUNT_DATA_AND_NOMBER = (15, 2)
ACCOUNT_CLIENT_NAME = (20, 11)