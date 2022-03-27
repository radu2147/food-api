from datetime import datetime
from typing import List

from pydantic.main import BaseModel

from model.meal import Meal
from model.user import User


class Repository(BaseModel):

    lista: List[Meal] = []
    __id: int = 0

    def __generate_id(self) -> int:
        self.__id += 1
        return self.__id

    def add(self, el):
        el.id = self.__generate_id()
        self.lista.append(el)

    def remove(self, id: int):
        self.lista = [el for el in self.lista if el.id != id]

    def filter_by_date(self, date: datetime, current_user: User) -> List[Meal]:
        return [el for el in self.lista if el.date.date() == date.date() and el.user == current_user]