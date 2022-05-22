from typing import Optional
from sqlalchemy.orm import Session
from model.user import DbUser, User

class DbUserRepository:

    def exists(self, db: Session, user: str) -> bool:
        rez = db.query(DbUser).filter(DbUser.username == user)
        return len(rez.all()) == 1

    def get(self, db: Session, user: str) -> Optional[User]:
        rez = db.query(DbUser).filter(DbUser.username == user)
        all = rez.all()
        if len(all) == 0:
            return None
        return User(username=all[0].username, password=all[0].hashed_password)

    def add_user(self, db: Session, user: User) -> Optional[User]:
        if self.exists(db, user.username):
            return None
        db_user = DbUser(username=user.username, hashed_password=user.password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user