from pydantic import BaseModel
from app.models.response import Response

class NotiRequest(BaseModel):
    temperature:float

class _NotiResponse(BaseModel):
    temperature:float
    user_id: str

class NotiResponse(Response):
    data: _NotiResponse | list[_NotiResponse] | dict