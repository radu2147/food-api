class Prediction:
    def __init__(self, food_class: str, kcal: float, carbs: float, protein: float, fat: float):
        self.__food_class = food_class
        self.__kcal = kcal
        self.__carbs = carbs
        self.__protein = protein
        self.__fat = fat

    def to_map(self):
        return {'foodClass': self.__food_class, 'kcal': self.__kcal, 'carbs': self.__carbs, 'protein': self.__protein,
                'fat': self.__fat}
