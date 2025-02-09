# Створіть Final клас Config, щоб заборонити його наслідування.
# Реалізуйте абстрактний клас BaseRepository, який має метод save(data: Dict[str, Any]) -> None.
# Реалізуйте SQLRepository, який наслідує BaseRepository та перевизначає save().
from abc import ABC, abstractmethod
from typing import Final, Dict, Any


class Config:
    URL: Final[str] = "http://my.com"


class BaseRepository(ABC):
    @abstractmethod
    def save(self, data: Dict[str, Any]) -> None:
        pass


class SQLRepository(BaseRepository):
    def save(self, data: Dict[str, Any]) -> None:
        print("Save!!!!")


if __name__ == "__main__":
    repo = SQLRepository()
    repo.save({"name": "Product1", "price": 10.5})
