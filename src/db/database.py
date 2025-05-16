import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI
from tortoise.contrib.fastapi import RegisterTortoise

from src.config.settings import settings


logger = logging.getLogger(__name__)


TORTOISE_ORM = {
    "connections": {
        "default": settings.db.DATABASE_URL,
    },
    "apps": {
        "models": {
            "models": [
                "src.models.user",
                "src.models.notification",
            ],
            "default_connection": "default",
        },
    },
}


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    logger.info(settings.db.DATABASE_URL)
    async with RegisterTortoise(
        app,
        config=TORTOISE_ORM,
        generate_schemas=True,
        add_exception_handlers=True,
    ):
        yield
