class Prediction:
    def __init__(self, prediction: float, food_class: str):
        self.__prediction = prediction
        self.__food_class = food_class

    def to_map(self):
        return {"prediction": self.__prediction, 'foodClass': self.__food_class}