from pydantic import BaseModel
from app.models.response import Response
from typing import Union, List, Optional

class NotiRequest(BaseModel):
    temperature:float

class _NotiResponse(BaseModel):
    temperature:float
    user_id: str

class NotiResponse(Response):
    data: List[_NotiResponse]