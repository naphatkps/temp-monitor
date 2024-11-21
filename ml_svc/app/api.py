from app.model import ForcastModel
from app.config import config
from fastapi import APIRouter
from app.schema import PredictionRequest, PredictionResponse

router = APIRouter()
model = ForcastModel(config.MODEL_PATH)

@router.post("/predict/", response_model=PredictionResponse)
async def predict_temperature(data: PredictionRequest):
    prediction = model.predict(data)
    return {"prediction_temperatures": prediction}