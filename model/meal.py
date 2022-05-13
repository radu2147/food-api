from sqlalchemy import Column, DateTime, Enum, Integer, String, null
from model.base import Base
from model.meal_type import MealType
from model.nutritional_values import NutritionalValues
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy.orm import relationship

from model.user import User


class Meal(BaseModel):
    id: int
    name: str
    nutritional_values: NutritionalValues
    meal_type: MealType
    date: datetime
    user: User
    quantity: int

class DbMeal(Base):
    id = Column(Integer, primary_key = True, index = True)
    name = Column(String, null = False)
    quantity = Column(Integer, null = False)
    date = Column(DateTime, null = False)
    meal_type = Column(Enum(MealType), null=False)
    
    kcal = Column(Integer, null = False)
    protein = Column(Integer, null = False)
    carbs = Column(Integer, null = False)
    fat = Column(Integer, null = False)

    user = relationship("DbMeal", back_populates="owner")
    
