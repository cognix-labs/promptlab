from abc import ABC, abstractmethod


class Target(ABC):
    @abstractmethod
    def run(self, data: dict):
        pass
