from abc import ABC, abstractmethod


class AddressReader(ABC):
    @abstractmethod
    def read(self, path):
        pass