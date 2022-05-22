from datetime import datetime
from typing import List

from pydantic.main import BaseModel
from model.base import SessionLocal

from model.meal import DbMeal, Meal
from model.user import DbUser, User
from sqlalchemy.orm import Session

class DbMealRepository:

    def filter_by_date(self, db: Session, date: datetime, current_user: User) -> List[Meal]:
        rez = db.query(DbMeal).filter(DbMeal.date == self.__parse_date(date), DbMeal.username == current_user.username).all()
        return [Meal.fromDb(el) for el in rez]

    def __parse_date(self, date: datetime) -> datetime:
        return datetime.combine(date.date(), datetime.today().min.time())

    def add(self, db: Session, el: Meal):
        db_meal = DbMeal(
            name=el.name,
            quantity=el.quantity,
            date=self.__parse_date(el.date),
            meal_type=el.meal_type,
            kcal=el.kcal,
            protein=el.protein,
            carbs=el.carbs,
            fat=el.fat,
            username=el.user.username
        )
        db.add(db_meal)
        db.commit()
        db.refresh(db_meal)