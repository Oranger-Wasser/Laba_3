from dataclasses import dataclass


@dataclass(frozen=True)
class Address:
    city: str
    street: str
    house: str
    floor: int