"""FastApi app module."""

from fastapi import FastAPI
from tortoise.contrib.fastapi import tortoise_exception_handlers

from src.db.database import lifespan

from src.routers.exception_handlers import exception_handlers
from src.routers.healthcheck import healthcheck_router
from src.routers.notifications_router import notifications_router
from src.routers.users_router import user_router

exception_handlers.update(tortoise_exception_handlers())

app = FastAPI(
    exception_handlers=exception_handlers,
    lifespan=lifespan,
)

app.include_router(notifications_router, prefix="/notifications", tags=["notifications"])
app.include_router(user_router, prefix='/api')
app.include_router(healthcheck_router, prefix='/api')
