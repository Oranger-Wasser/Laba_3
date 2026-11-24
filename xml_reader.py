from xml.parsers import expat

from address import Address
from address_reader import AddressReader


class XmlAddressReader(AddressReader):
    def read(self, path):
        parser = expat.ParserCreate()
        required_fields = {"city", "street", "house", "floor"}
        addresses = []
        depth = 0

        def start_element(tag, fields):
            nonlocal depth
            depth += 1
            line = parser.CurrentLineNumber

            if depth == 1:
                if tag != "root":
                    raise ValueError(f"Строка {line}: корневой тег должен быть <root>.")
                return

            if depth != 2 or tag != "item":
                raise ValueError(f"Строка {line}: ожидается запись <item> внутри <root>.")

            if fields.keys() != required_fields or any(not value.strip() for value in fields.values()):
                raise ValueError(f"Строка {line}: нужны город, улица, номер дома и этажность.")

            try:
                floor = int(fields["floor"])
            except ValueError:
                raise ValueError(f"Строка {line}: этажность должна быть целым числом.") from None

            if floor < 1:
                raise ValueError(f"Строка {line}: этажность должна быть больше нуля.")

            addresses.append(
                Address(
                    city=fields["city"],
                    street=fields["street"],
                    house=fields["house"],
                    floor=floor,
                )
            )

        def end_element(_tag):
            nonlocal depth
            depth -= 1

        parser.StartElementHandler = start_element
        parser.EndElementHandler = end_element

        with path.open("rb") as xml_file:
            try:
                while chunk := xml_file.read(64 * 1024):
                    parser.Parse(chunk, False)
                    yield from addresses
                    addresses.clear()
                parser.Parse(b"", True)
            except expat.ExpatError as error:
                raise ValueError(f"Строка {error.lineno}: неверный формат XML.") from error