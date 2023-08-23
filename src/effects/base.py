from abc import ABC, abstractmethod
from config import Config
from connection import Connection


class BaseEffect(ABC):
    def __init__(self, config: Config, connection: Connection) -> None:
        self.config = config
        self.connection = connection
        self.init()

    @abstractmethod
    def init(self):
        pass

    @abstractmethod
    def update(self):
        pass
