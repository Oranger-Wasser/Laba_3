from address_statistics import StatisticsCalculator
from console_app import ConsoleApp
from csv_reader import CsvAddressReader
from xml_reader import XmlAddressReader


def main():
    readers = {
        ".csv": CsvAddressReader(),
        ".xml": XmlAddressReader(),
    }
    app = ConsoleApp(readers, StatisticsCalculator())
    app.run()


if __name__ == "__main__":
    main()