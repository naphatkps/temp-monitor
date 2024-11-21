from dotenv import load_dotenv

load_dotenv("./app/.env")

import os

class Config:
    API_URL = os.getenv("API_URL")
    DATABASE_URL = os.getenv("DATABASE_URL")
    GEO_API_KEY = os.getenv("GEO_API_KEY")  
    ML_SERVICE_URL = os.getenv("ML_SERVICE_URL")
    LOGGER_SERVICE_URL = os.getenv("LOGGER_SERVICE_URL")
    COORDINATE_API_URL = os.getenv("COORDINATE_API_URL")


config = Config()