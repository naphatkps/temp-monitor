from pydantic import BaseModel
from app.models.response import Response
from typing import Union, List, Optional

class WeatherRequest(BaseModel):
    city: str
    country: str

class _WeatherResponse(BaseModel):
    time: str
    temperature_2m: float
    rain: float

class WeatherResponse(Response):
    data: List[_WeatherResponse]