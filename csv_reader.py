import csv

from address import Address
from address_reader import AddressReader


class CsvAddressReader(AddressReader):
    def read(self, path):
        with path.open(encoding="utf-8-sig", newline="") as csv_file:
            rows = csv.DictReader(csv_file, delimiter=";")

            for row in rows:
                floor = int(row["floor"])
                yield Address(
                    city=row["city"],
                    street=row["street"],
                    house=row["house"],
                    floor=floor,
                )