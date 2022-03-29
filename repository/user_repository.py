from typing import List, Optional, Dict

from pydantic.main import BaseModel

from model.user import User


class UserRepository:

    def __init__(self) -> None:
        self.lista: Dict[str, User] = {}

    def __contains__(self, user: str) -> bool:
        return user in self.lista

    def __getitem__(self, item: str) -> Optional[User]:
        if item in self.lista:
            return self.lista[item]
        return None

    def add_user(self, user: User) -> Optional[User]:
        if user.username in self.lista:
            return None
        self.lista[user.username] = user
        return user