from fastapi import FastAPI
from app.database import db
from app.config import config
from app.api import user, weather
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from app.api.weather import predict_weather,predict

import requests

app = FastAPI()

app.include_router(user.router)
app.include_router(weather.router)

collection = db['users']

logger_URL = "http://localhost/logger/api/v1/logger"

def my_daily_task():
    print("This is a daily task that runs every 6 hour")

    response = predict()["predicted_temperatures"]
    # print(type(response))
    avg_temp = sum(response)/len(response)
    # print(avg_temp)
    # print(response)

    users = list(collection.find({}, {"email": 1, "_id": 0}))
    # print(users)
    for user in users:
        # print(user["email"])
        response = requests.post(
            "http://noti-weather-service.default.svc.cluster.local:8888/noti",
            json={
                "username": "user",
                "email": str(user["email"]),
                "temperature": str(avg_temp)+" C",
            }
        )
        logger_data = {
            "text" : str(user["email"]) + " has been notified"
        }
        # requests.post(logger_URL, json=logger_data)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True, # 
    allow_methods=["*"],
    allow_headers=["*"],
)

scheduler = BackgroundScheduler()
trigger = CronTrigger(hour="0,6,12,18", minute=0)
scheduler.add_job(my_daily_task, trigger)
scheduler.start()

# app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    scheduler.shutdown()

