from fastapi import APIRouter
from app.database import db
from app.models.user import UserRequest, UserResponse
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from app.config import config
import requests

router = APIRouter()
collection = db['users']
logger_url = config.LOGGER_SERVICE_URL

def convert_object_id(item):
    """Convert ObjectId fields to strings in a MongoDB document."""
    if isinstance(item, list):
        for doc in item:
            if "_id" in doc:
                doc["_id"] = str(doc["_id"])
    elif item and "_id" in item:
        item["_id"] = str(item["_id"])
    return item

@router.post("/users/", response_model=UserResponse)
async def create_user(user: UserRequest):
    user_data = jsonable_encoder(user)
    if collection.find_one({"email": user_data["email"]}):
        response = UserResponse(
            success=False,
            message="Email already exists",
            data=[]
        )
        status_code = 400
        log_data = {
            "service": "backend",
            "level": "Error",
            "message": user_data["email"] + " already exists",
        }
        requests.post(logger_url, json=log_data)
    else:
        user_id = collection.insert_one(user_data).inserted_id
        response = UserResponse(
            success=True,
            message="User created successfully",
            data=[user_data]
        )
        status_code = 201
        log_data = {
            "service": "backend",
            "level": "Info",
            "message": user_data["email"] + ", " + str(user_id) + " created successfully",
        }
        requests.post(logger_url, json=log_data)
    return JSONResponse(content=response.model_dump(), status_code=status_code)

@router.get("/users/", response_model=UserResponse)
async def get_users():
    try:
        users = list(collection.find({}, {"_id": 0}))
        users = [convert_object_id(user) for user in users]
        response = UserResponse(
            success=True,
            message="Users fetched successfully",
            data=users
        )
        status_code = 200
        log_data = {
            "service": "backend",
            "level": "Info",
            "message": "Users fetched successfully",
        }
        requests.post(logger_url, json=log_data)
    except Exception as e:
        response = UserResponse(
            success=False,
            message="Failed to fetch users",
            data=[]
        )
        status_code = 500
        log_data = {
            "service": "backend",
            "level": "Error",
            "message": str(e),
        }
        requests.post(logger_url, json=log_data)
    return JSONResponse(content=response.model_dump(), status_code=status_code)
