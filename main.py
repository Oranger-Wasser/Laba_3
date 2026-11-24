from pathlib import Path

from csv_reader import CsvAddressReader
from xml_reader import XmlAddressReader


def main():
    folder = Path(__file__).parent
    readers = {
        "address.csv": CsvAddressReader(),
        "address.xml": XmlAddressReader(),
    }

    for filename, reader in readers.items():
        count = 0
        for _ in reader.read(folder / filename):
            count += 1

        print(filename, "— прочитано записей:", count)


if __name__ == "__main__":
    main()