import csv

from address import Address
from address_reader import AddressReader


class CsvAddressReader(AddressReader):
    def read(self, path):
        with path.open(encoding="utf-8-sig", newline="") as csv_file:
            rows = csv.reader(csv_file, delimiter=";", strict=True)

            try:
                header = next(rows, [])
                required_fields = {"city", "street", "house", "floor"}
                if len(header) != len(required_fields) or set(header) != required_fields:
                    raise ValueError("Строка 1: ожидаются столбцы city, street, house и floor.")

                for row in rows:
                    if not row:
                        continue

                    line = rows.line_num
                    if len(row) != len(header) or any(not value.strip() for value in row):
                        raise ValueError(f"Строка {line}: нужны город, улица, номер дома и этажность.")

                    fields = dict(zip(header, row))
                    try:
                        floor = int(fields["floor"])
                    except ValueError:
                        raise ValueError(f"Строка {line}: этажность должна быть целым числом.") from None

                    if floor < 1:
                        raise ValueError(f"Строка {line}: этажность должна быть больше нуля.")

                    yield Address(
                        city=fields["city"],
                        street=fields["street"],
                        house=fields["house"],
                        floor=floor,
                    )
            except csv.Error as error:
                raise ValueError(f"Строка {rows.line_num}: неверный формат CSV.") from error