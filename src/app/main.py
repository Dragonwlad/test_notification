"""FastApi app module."""

from fastapi import FastAPI
from tortoise.contrib.fastapi import tortoise_exception_handlers

from src.db.database import lifespan

from starlette.middleware.base import BaseHTTPMiddleware

# from src.app.events import shutdown_event, startup_event
from src.app.middlewares import logging_middleware, process_time_header_middleware
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
# app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(user_router, prefix='/api')
app.include_router(healthcheck_router, prefix='/api')

# noinspection PyTypeChecker
# app.add_middleware(BaseHTTPMiddleware, dispatch=logging_middleware)
# noinspection PyTypeChecker
# app.add_middleware(BaseHTTPMiddleware, dispatch=process_time_header_middleware)


# app.add_event_handler('startup', startup_event)
# app.add_event_handler('shutdown', shutdown_event)
