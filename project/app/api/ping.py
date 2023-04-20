from typing import Annotated

from fastapi import APIRouter, Depends

from app.config import Settings, get_settings

router = APIRouter()


@router.get("/test")
async def ping(settings: Annotated[Settings, Depends(get_settings)]):
    return {
        "message": "pong",
        "env": settings.environment,
        "testing": settings.testing,
    }
