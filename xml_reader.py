import xml.etree.ElementTree as ET

from address import Address
from address_reader import AddressReader


class XmlAddressReader(AddressReader):
    def read(self, path):
        with path.open("rb") as xml_file:
            events = ET.iterparse(xml_file, events=("start", "end"))
            _, root = next(events)

            for event, item in events:
                if event == "end" and item.tag == "item":
                    address = Address(
                        city=item.attrib["city"],
                        street=item.attrib["street"],
                        house=item.attrib["house"],
                        floor=int(item.attrib["floor"]),
                    )
                    root.remove(item)
                    yield address