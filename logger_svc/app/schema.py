from pydantic import BaseModel

class LogRequest(BaseModel):
    service: str
    level: str
    message: str

class LogResponse(BaseModel):
    message: str
    status: str