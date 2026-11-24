from csv import Error as CsvError
from pathlib import Path
from time import perf_counter
from xml.etree.ElementTree import ParseError


class ConsoleApp:
    def __init__(self, readers, calculator):
        self.readers = readers
        self.calculator = calculator

    def run(self):
        while True:
            try:
                path_text = input("Введи путь к CSV или XML либо exit: ").strip().strip('"')
            except (EOFError, KeyboardInterrupt):
                print("\nРабота завершена.")
                return

            if path_text.lower() == "exit":
                print("Работа завершена.")
                return

            if not path_text:
                print("Введи путь к файлу.")
                continue

            path = Path(path_text)

            try:
                if not path.is_file():
                    print("Файл не найден или указан путь к папке.")
                    continue

                reader = self.readers.get(path.suffix.lower())
                if reader is None:
                    print("Поддерживаются только файлы .csv и .xml.")
                    continue

                start = perf_counter()
                report = self.calculator.calculate(reader.read(path))
                elapsed = perf_counter() - start

            except (OSError, ValueError, KeyError, CsvError, ParseError) as error:
                print(f"Ошибка обработки файла: {error}")
                continue

            print(f"\nФайл: {path.name}")
            self.print_report(report)
            print(f"\nВремя обработки: {elapsed:.3f} с\n")

    def print_report(self, report):
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