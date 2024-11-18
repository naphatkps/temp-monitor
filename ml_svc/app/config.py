from dotenv import load_dotenv

load_dotenv("./app/.env")

import os

class Config:
    MODEL_PATH = os.getenv("MODEL_PATH")
    BACKEND_SERVICE_URL = os.getenv("BACKEND_SERVICE_URL")

config = Config()