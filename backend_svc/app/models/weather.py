from pydantic import BaseModel
from app.models.response import Response

class WeatherRequest(BaseModel):
    city: str
    country: str

class _WeatherResponse(BaseModel):
    time: str
    temperature_2m: float
    rain: float

class WeatherResponse(Response):
    data: _WeatherResponse | list[_WeatherResponse] | dict