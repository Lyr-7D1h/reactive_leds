from abc import ABC, abstractmethod
from config import Config


class BaseEffect(ABC):
    def __init__(self, config: Config) -> None:
        self.config = config
        self.init()

    @abstractmethod
    def init(self):
        pass

    @abstractmethod
    def update(self):
        pass
