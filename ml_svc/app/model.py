import pickle
import numpy as np
from app.schema import PredictionRequest

class ForcastModel:
    def __init__(self, path):
        with open(path, "rb") as f:
            self.model = pickle.load(f)

    def predict(self, data: PredictionRequest) -> list[float]:
        temperatures = data.temperatures

        if len(temperatures) != 168:
            raise RuntimeError("Input data must contain exactly 168 hourly temperature readings.")

        try:
            temperatures = list(map(float, temperatures))
        except ValueError as e:
            raise RuntimeError("Input data must contain only numbers. : " + str(e))
        
        try:
            temperatures = np.array(temperatures).reshape(1, -1)
            prediction = self.model.predict(temperatures)
            return prediction.tolist()[0]
        except Exception as e:
            raise RuntimeError("An error occurred while predicting the temperature. : " + str(e))