from typing import Annotated
from fastapi import FastAPI, Depends
from .config import get_settings, Settings

app = FastAPI()

@app.get("/test")
async def ping(settings: Annotated[Settings, Depends(get_settings)]):
    return {
        "message": "pong",
        "env": settings.environment,
        "testing": settings.testing,
        }
