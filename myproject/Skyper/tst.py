import re
from datetime import datetime

class InvoiceNameDetailsExtractor:
    def __init__(self, input_string):
        self.input_string = input_string
        self.parsed_data = self.parsing_file()

    def parsing_file(self):
        number_pattern = r'№ (\d+)'
        date_pattern = r'(\d{1,2}) (\w+) (\d{4})'

        number = re.search(number_pattern, self.input_string).group(1)
        day, month_name, year = re.search(date_pattern, self.input_string).groups()

        return [number, day, month_name, year]

    @staticmethod
    def date_formating(*date_data):
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
        result = self.date_formating(*self.parsed_data)
        return result[0]

    def date_in_datefield(self):
        result = self.date_formating(*self.parsed_data)
        return result[1]

    def number_invoice(self):
        result = self.date_formating(*self.parsed_data)
        return result[2]

input_string = "Видаткова накладна № 1592 від 03 серпня 2023 р."
work = InvoiceNameDetailsExtractor(input_string)
number_inv = work.number_invoice()
date_ = work.date_in_datefield()
print("Номер накладной:", number_inv)
print("Дата:", date_)
