from dataclasses import dataclass


@dataclass
class StatisticsReport:
    duplicates: dict
    floors_by_city: dict


class StatisticsCalculator:
    def calculate(self, addresses):
        counts = {}
        floors_by_city = {}

        for address in addresses:
            counts[address] = counts.get(address, 0) + 1

            if counts[address] == 1:
                city = address.city
                floor = address.floor

                if city not in floors_by_city:
                    floors_by_city[city] = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}

                if 1 <= floor <= 5:
                    floors_by_city[city][floor] += 1

        duplicates = {}
        for address, count in counts.items():
            if count > 1:
                duplicates[address] = count

        return StatisticsReport(duplicates, floors_by_city)