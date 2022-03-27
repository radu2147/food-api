from model.meal_type import MealType
from model.nutritional_values import NutritionalValues
from pydantic import BaseModel
from datetime import datetime

from model.user import User


class Meal(BaseModel):
    id: int
    name: str
    nutritional_values: NutritionalValues
    meal_type: MealType
    date: datetime
    user: User
