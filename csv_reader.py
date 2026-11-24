import csv

from address import Address
from address_reader import AddressReader


class CsvAddressReader(AddressReader):
    def read(self, path):
        fields = ("city", "street", "house", "floor")

        with path.open(encoding="utf-8-sig", newline="") as csv_file:
            rows = csv.reader(csv_file, delimiter=";", strict=True)

            try:
                header = next(rows, [])
                if sorted(header) != sorted(fields):
                    raise ValueError("Строка 1: нужны столбцы city, street, house и floor.")

                columns = [header.index(field) for field in fields]

                for row in rows:
                    if not row:
                        continue

                    line = rows.line_num
                    if len(row) != len(fields) or any(not value.strip() for value in row):
                        raise ValueError(f"Строка {line}: нужны четыре заполненных поля.")

                    city, street, house, floor_text = (row[column] for column in columns)
                    try:
                        floor = int(floor_text)
                    except ValueError:
                        raise ValueError(f"Строка {line}: этажность должна быть целым числом.") from None

                    if floor < 1:
                        raise ValueError(f"Строка {line}: этажность должна быть больше нуля.")

                    yield Address(city, street, house, floor)
            except csv.Error as error:
                raise ValueError(f"Строка {rows.line_num}: неверный формат CSV.") from error