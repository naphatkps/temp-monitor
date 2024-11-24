from app.config import config
from fastapi import APIRouter
from app.schema import LogRequest, LogResponse
from datetime import datetime

router = APIRouter()

@router.get("/health/")
async def health_check():
    return {"status": "ok"}

@router.post("/log/")
async def log(request: LogRequest):
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{time}] {request.service} :: {request.level} :: {request.message}"
    print(log_message)
    return LogResponse(
        message="Logged message",
        status="ok"
    )

