from fastapi import APIRouter
from app.models.weather import WeatherRequest, WeatherResponse
import openmeteo_requests
import requests_cache
from retry_requests import retry
from datetime import datetime, timedelta
import requests
from app.config import config
import pandas as pd
from fastapi.responses import JSONResponse

router = APIRouter()

model_url = config.ML_SERVICE_URL
logger_url = config.LOGGER_SERVICE_URL
api_key = config.GEO_API_KEY
url = config.API_URL
coordinate_url = config.COORDINATE_API_URL

cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

@router.post('/current_weather/', response_model=WeatherResponse) 
async def get_current_weather(request: WeatherRequest):
    try:
        response = requests.get(coordinate_url, 
                                params={"city": request.city, "country": request.country},
                                headers={"x-api-key": api_key})
    except Exception as e:
        response = WeatherResponse(
            data={},
            success=False,
            message="Failed to fetch coordinates"
        )
        status_code = 500
        return JSONResponse(content=response.model_dump(), status_code=status_code)
    
    latitude = response.json()[0]["latitude"]
    longitude = response.json()[0]["longitude"]
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": ["temperature_2m", "rain"]
    }

    try:
        responses = openmeteo.weather_api(config.API_URL, params=params)
        response = responses[0]
        current = response.Current()
        current_temperature_2m = current.Variables(0).Value()
        current_rain = current.Variables(1).Value()
        status_code = 200

        response = WeatherResponse(
            data={
                "time": datetime.now().isoformat(),
                "temperature_2m": current_temperature_2m,
                "rain": current_rain
            },
            success=True,
            message="Current weather fetched successfully"
        )
    except Exception as e:
        response = WeatherResponse(
            data={},
            success=False,
            message="Failed to fetch current weather"
        )
        status_code = 500

    return JSONResponse(content=response.model_dump(), status_code=status_code)

@router.post('/predict_weather/', response_model=WeatherResponse)
async def predict_weather(request: WeatherRequest):
    try:
        res = predict(request)
        response = WeatherResponse(
            data=res,
            success=True,
            message="Weather prediction fetched successfully"
        )
        status_code = 200
    except Exception as e:
        response = WeatherResponse(
            data={},
            success=False,
            message=e
        )
        status_code = 500

    return JSONResponse(content=response.model_dump(), status_code=status_code)

def predict(request: WeatherRequest):
    response = requests.get(coordinate_url, 
                            params={"city": request.city, "country": request.country},
                            headers={"x-api-key": api_key})
    latitude = response.json()[0]["latitude"]
    longitude = response.json()[0]["longitude"]

    today = datetime.now()
    end_date = today.strftime("%Y-%m-%d")
    start_date = today - timedelta(hours=168)
    start_date = start_date.strftime("%Y-%m-%d")

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
	    "end_date": end_date,
	    "hourly": "temperature_2m"
    }

    try:
        responses = openmeteo.weather_api(url, params=params)
    except Exception as e:
        raise "Failed to fetch weather data"

    try:
        response = responses[0]
        hourly = response.Hourly()
        hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
        hourly_data = {"date": pd.date_range(
            start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
            end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
            freq = pd.Timedelta(seconds = hourly.Interval()),
            inclusive = "left"
        )}
        hourly_data["temperature_2m"] = hourly_temperature_2m
        hourly_dataframe = pd.DataFrame(hourly_data)
        current = datetime.now()
        current = current.replace(minute=0, second=0, microsecond=0)
        current = pd.to_datetime(current, utc = True)

        start_time = current - timedelta(hours=167)

        hourly_dataframe = hourly_dataframe[(hourly_dataframe['date'] >= start_time) & (hourly_dataframe['date'] <= current)]

        hourly_temperature_2m = hourly_dataframe['temperature_2m'].tolist()

        try:
            model_response = requests.post(model_url, json={"temperatures": hourly_temperature_2m})
            response_data = []
            for i in range(len(model_response.json()["prediction_temperatures"])):
                response_data.append({
                    "time": ( current + timedelta(hours=i) ).isoformat(),
                    "temperature_2m": model_response.json()["prediction_temperatures"][i],
                    "rain": -1
                })
        except Exception as e:
            raise "Failed to fetch weather prediction"
    except Exception as e:
        raise "Failed to process weather data"
    return response_data