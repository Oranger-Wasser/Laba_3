import xml.etree.ElementTree as ET

from address import Address
from address_reader import AddressReader


class XmlAddressReader(AddressReader):
    def read(self, path):
        root = ET.parse(path).getroot()
        required_fields = {"city", "street", "house", "floor"}

        for number, item in enumerate(root, start=1):
            if len(item) > 0:
                raise ValueError(f"Запись №{number}: вложенные теги не допускаются.")

            fields = item.attrib
            if fields.keys() != required_fields or any(not value.strip() for value in fields.values()):
                raise ValueError(f"Запись №{number}: нужны город, улица, номер дома и этажность.")

            try:
                floor = int(fields["floor"])
            except ValueError:
                raise ValueError(f"Запись №{number}: этажность должна быть целым числом.") from None

            if floor < 1:
                raise ValueError(f"Запись №{number}: этажность должна быть больше нуля.")

            yield Address(
                city=fields["city"],
                street=fields["street"],
                house=fields["house"],
                floor=floor,
            )