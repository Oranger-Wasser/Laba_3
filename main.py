from pathlib import Path

from csv_reader import CsvAddressReader


def main():
    path = Path(__file__).parent / "address.csv"
    reader = CsvAddressReader()

    count = 0
    for _ in reader.read(path):
        count += 1

    print("Прочитано записей:", count)


if __name__ == "__main__":
    main()