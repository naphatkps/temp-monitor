from fastapi import APIRouter
from app.database import db
from fastapi.responses import JSONResponse
from app.config import config
from app.models.noti import NotiRequest, NotiResponse
import requests
from bson import ObjectId

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from app.api.weather import predict
from app.models.weather import WeatherRequest

router = APIRouter()
noti_url = config.NOTI_SERVICE_URL

api_key = config.GEO_API_KEY
coordinate_url = config.COORDINATE_API_URL

collection = db['users']

@router.post("/noti/{user_id}", response_model=NotiResponse)
async def noti_user(user_id: str, noti: NotiRequest):
    user = db['users'].find_one({"_id": ObjectId(user_id)})
    if user:
        try:
            print(user)
            print(noti)
            response = requests.post(
                noti_url,
                json={
                    "username": user["name"],
                    "email": user["email"],
                    "temperature": noti.temperature
                }
            )
            response = NotiResponse(
                success=True,
                message="User notified successfully",
                data=[{"temperature": noti.temperature, "user_id": user_id}]
            )
            status_code = 200
            logger_data = {
                "service": "backend",
                "level": "Info",
                "message": "User notified successfully",
            }
            requests.post(config.LOGGER_SERVICE_URL, json=logger_data)
        except Exception as e:
            print(e)
            response = NotiResponse(
                success=False,
                message="Failed to notify user",
                data=[]
            )
            status_code = 500
            logger_data = {
                "service": "backend",
                "level": "Error",
                "message": str(e),
            }
        requests.post(config.LOGGER_SERVICE_URL, json=logger_data)
    else:
        response = NotiResponse(
            success=False,
            message="User not found",
            data=[]
        )
        status_code = 404
        logger_data = {
            "service": "backend",
            "level": "Error",
            "message": "User not found",
        }
        requests.post(config.LOGGER_SERVICE_URL, json=logger_data)
    return JSONResponse(content=response.model_dump(), status_code=status_code)

@router.post("/noti/", response_model=NotiResponse)
async def noti_all_users(noti: NotiRequest):
    try:
        users = list(collection.find({}, {"email": 1, "name": 1, "_id": 1}))
        data = []
        for user in users:
            try:
                print(user)
                response = requests.post(
                    noti_url,
                    json={
                        "username": user["name"],
                        "email": user["email"],
                        "temperature": noti.temperature
                    }
                )
                data.append({"user_id": str(user["_id"]), "temperature": noti.temperature})
            except Exception as e:
                logger_data = {
                    "service": "backend",
                    "level": "Error",
                    "message": str(e),
                }
                requests.post(config.LOGGER_SERVICE_URL, json=logger_data)
        response = NotiResponse(
            success=True,
            message="Users notified successfully",
            data=data
        )
        status_code = 200
        logger_data = {
            "service": "backend",
            "level": "Info",
            "message": "Users notified successfully",
        }
        requests.post(config.LOGGER_SERVICE_URL, json=logger_data)
    except Exception as e:
        response = NotiResponse(
            success=False,
            message="Failed to notify users",
            data=[]
        )
        status_code = 500
        logger_data = {
            "service": "backend",
            "level": "Error",
            "message": str(e),
        }
        requests.post(config.LOGGER_SERVICE_URL, json=logger_data)
    return JSONResponse(content=response.model_dump(), status_code=status_code)

@router.get("/noti/")
async def task():
    users = list(collection.find({}, {"email": 1, "_id": 1, "city": 1, "country": 1}))
    places = dict()

    for user in users:
        place = user["city"] + "_" + user["country"]
        places[place] = 0

    for place in places:
        city, country = place.split("_")
        req = WeatherRequest(city=city, country=country)
        response = predict(request=req)
        avg_temp = 0
        avg_rain = 0
        for res in response:
            avg_temp += res["temperature_2m"]
            avg_rain += res["rain"]
        places[place] = {"temperature": avg_temp/len(response), "rain": avg_rain/len(response)}
    
    for user in users:
        place = user["city"] + "_" + user["country"]
        response = await noti_user(user_id=str(user["_id"]), noti=NotiRequest(temperature=places[place]["temperature"]))

    logger_data = {
        "service": "backend",
        "level": "Info",
        "message": "Users notified successfully",
    }
    requests.post(config.LOGGER_SERVICE_URL, json=logger_data)
