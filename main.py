from pathlib import Path

from address_statistics import StatisticsCalculator
from csv_reader import CsvAddressReader
from xml_reader import XmlAddressReader


def print_report(report):
    print("Повторяющиеся записи:")
    if report.duplicates:
        for address, count in report.duplicates.items():
            print(
                f"{address.city}, {address.street}, дом {address.house}, "
                f"этажей: {address.floor} — найдено записей: {count}"
            )
    else:
        print("Повторяющихся записей нет.")

    print("\nДома по городам:")
    for city, floors in sorted(report.floors_by_city.items()):
        print(city)
        for floor in range(1, 6):
            print(f"  {floor} эт. — {floors[floor]}")


def main():
    folder = Path(__file__).parent
    readers = {
        "address.csv": CsvAddressReader(),
        "address.xml": XmlAddressReader(),
    }
    calculator = StatisticsCalculator()

    for filename, reader in readers.items():
        addresses = reader.read(folder / filename)
        report = calculator.calculate(addresses)

        print("\nФайл:", filename)
        print_report(report)


if __name__ == "__main__":
    main()