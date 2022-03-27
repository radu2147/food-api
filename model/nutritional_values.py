from pydantic import BaseModel


class NutritionalValues(BaseModel):
    kcal: float
    protein: float
    carbs: float
    fats: float
