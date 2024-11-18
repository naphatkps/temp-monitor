from fastapi import FastAPI
from app.api import router
from fastapi.middleware.cors import CORSMiddleware
from app.config import config

app = FastAPI()
app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[config.BACKEND_SERVICE_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)