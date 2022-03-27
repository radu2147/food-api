from enum import Enum


class MealType(str, Enum):
    Breakfast = "Breakfast",
    Lunch = "Lunch",
    Snack = "Snack",
    Dinner = "Dinner"
