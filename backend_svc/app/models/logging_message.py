from pydantic import BaseModel, Field

class LoggingMessage(BaseModel):
    id: str = Field(default=None, alias="_id")
    text: str
    