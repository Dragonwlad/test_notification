"""Module for running the Uvicorn server with custom logging configuration."""

import os
import sys

import uvicorn

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.app.main import app
from src.config.logger_setup import configure_logger
from src.config.settings import settings
from src.config.uvicorn_logger import build_uvicorn_log_config


def run():
    """Configure logging and run the ASGI application using uvicorn."""
    configure_logger(
        level=settings.logging.LOGGING_LEVEL,
        json_console_format=settings.logging.JSON_CONSOLE_FORMAT,
        json_file_format=settings.logging.JSON_FILE_FORMAT,
    )
    uvicorn_logger_config = build_uvicorn_log_config(
        level=settings.logging.LOGGING_LEVEL,
        json_console_format=settings.logging.JSON_CONSOLE_FORMAT,
        json_file_format=settings.logging.JSON_FILE_FORMAT,
    )
    uvicorn.run(
        app=app,
        host=settings.server.SERVER_HOST,
        port=settings.server.SERVER_PORT,
        log_config=uvicorn_logger_config,
        use_colors=True,
    )


if __name__ == '__main__':
    run()
