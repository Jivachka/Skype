import re
from datetime import datetime

class InvoiceDetailsExtractor:
    pass

class DateAndNumberExtractor(InvoiceDetailsExtractor):
    def __init__(self, input_string):
        self._input_string = input_string
        self._parsed_data = self.__parsing_file()
        super().__init__()

    def __parsing_file(self):
        number_pattern = r'№ (\d+)'
        date_pattern = r'(\d{1,2}) (\w+) (\d{4})'

        number = re.search(number_pattern, self._input_string).group(1)
        day, month_name, year = re.search(date_pattern, self._input_string).groups()

        return [number, day, month_name, year]

    @staticmethod
    def __date_formating(*date_data):
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
        result = self.__date_formating(*self._parsed_data)
        return result[0]

    def date_in_datefield(self):
        result = self.__date_formating(*self._parsed_data)
        return result[1]

    def number_invoice(self):
        result = self.__date_formating(*self._parsed_data)
        return result[2]

class Go:
    def __init__(self, __input_string):
        self.__input_string = __input_string
        # self.__input_string = "Видаткова накладна № 1592 від 03 серпня 2023 р."
        self.__work = DateAndNumberExtractor(self.__input_string)
        self.__number_inv = self.__work.number_invoice()
        self.__date_date_ = self.__work.date_in_datefield()
        self.__number_inv = self.__work.number_invoice()
        self.__date_ = self.__work.date_in_datefield()
        self.__number_faild = self.__work.date_in_str()

    def go_print(self):
        print("Номер накладной:", self.__number_inv)
        print("Дата:", self.__number_faild)
        print("Дата:", self.__date_)

if __name__ == "__main__":
    go_work = Go()
    go_work.go_print()
