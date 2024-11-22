from fastapi import FastAPI
from app.database import db
from app.api import user, weather, noti
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from app.api.noti import task

app = FastAPI()

app.include_router(user.router)
app.include_router(weather.router)
app.include_router(noti.router)

collection = db['users']

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True, # 
    allow_methods=["*"],
    allow_headers=["*"],
)

scheduler = BackgroundScheduler()
trigger = CronTrigger(minute=0)
scheduler.add_job(task, trigger)
scheduler.start()

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    scheduler.shutdown()

