from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey, Integer, String, null
from model.base import Base
from model.meal_type import MealType
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy.orm import relationship

from model.user import User

class DbMeal(Base):

    __tablename__ = 'meals'

    id = Column(Integer, primary_key = True, index = True)
    name = Column(String, nullable = False)
    quantity = Column(Integer, nullable = False)
    date = Column(DateTime, nullable = False)
    meal_type = Column(Enum(MealType), nullable=False)

    kcal = Column(Float, nullable = False)
    protein = Column(Float, nullable = False)
    carbs = Column(Float, nullable = False)
    fat = Column(Float, nullable = False)

    username = Column(String, ForeignKey('users.username'))

    user = relationship("DbUser", back_populates="meals")
    
class Meal(BaseModel):
    id: int
    name: str
    kcal: float
    carbs: float
    protein: float
    fat: float
    meal_type: MealType
    date: datetime
    user: User
    quantity: int

    @staticmethod
    def fromDb(meal: DbMeal) -> "Meal":
        return Meal(
            id=meal.id,
            name=meal.name,
            kcal=meal.kcal,
            carbs=meal.carbs,
            protein=meal.protein,
            fat=meal.fat,
            meal_type=meal.meal_type,
            date=meal.date,
            user=User.fromDb(meal.user),
            quantity=meal.quantity

        )

    class Config:
        orm_mode = True