import logging
from functools import lru_cache

from pydantic import AnyUrl, BaseSettings, Field

log = logging.getLogger("uvicorn")


class Settings(BaseSettings):
    environment: str | None = Field(default="dev")
    testing: bool = Field(default=False)
    db_url: AnyUrl = None


@lru_cache()
def get_settings() -> BaseSettings:
    log.info("Loading config from env")
    return Settings()
