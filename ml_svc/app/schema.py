from pydantic import BaseModel

class PredictionRequest(BaseModel):
    temperatures: list[float]

class PredictionResponse(BaseModel):
    prediction_temperatures: list[float]