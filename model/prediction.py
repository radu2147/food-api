from model.nutritional_values import NutritionalValues


class Prediction:
    def __init__(self, food_class: str, nutritional_values: NutritionalValues):
        self.__food_class = food_class
        self.__nutritional_values = nutritional_values

    def to_map(self):
        return {'foodClass': self.__food_class, 'nutritional_values': self.__nutritional_values}