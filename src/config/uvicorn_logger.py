"""Модуль для создания конфигураций журнала Uvicorn и пользовательских форматов.

Этот модуль предоставляет классы и функции для настройки журнала на серверах Uvicorn.
Он включает в себя различные классы форматера для ведения консоли и журнала файлов,
 поддерживая оба.
Форматы JSON и не JSON, а также функции для создания конфигураций журнала Uvicorn.
"""
import contextlib
import logging

import structlog
from structlog.types import EventDict

from src.config.logger_setup import build_default_processors
from src.config.settings import settings


class UvicornDefaultConsoleFormatter(structlog.stdlib.ProcessorFormatter):
    """Default console formatter for Uvicorn logs with structured logging."""

    def __init__(self, level, *args, **kwargs):
        """Initialize UvicornDefaultConsoleFormatter."""
        super().__init__(
            processor=structlog.dev.ConsoleRenderer(
                colors=True,
                # exception_formatter=structlog.dev.better_traceback,
            ),
            foreign_pre_chain=build_default_processors(level=level, json_format=False),
        )


class UvicornAccessConsoleFormatter(structlog.stdlib.ProcessorFormatter):
    """Access log console formatter for Uvicorn with structured logging."""

    def __init__(self, level, *args, **kwargs):
        """Initialize UvicornAccessConsoleFormatter."""
        processors = [
            _extract_uvicorn_request_meta,
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            structlog.dev.ConsoleRenderer(),
        ]

        # pass_foreign_args чтобы прокидывались значения из record.args в positional_args
        super().__init__(
            processors=processors,
            foreign_pre_chain=build_default_processors(level=level, json_format=False),
            pass_foreign_args=True,
        )


class UvicornDefaultJSONFormatter(structlog.stdlib.ProcessorFormatter):
    """Default JSON formatter for Uvicorn logs with structured logging."""

    def __init__(self, level, *args, **kwargs):
        """Initialize UvicornDefaultJSONFormatter."""
        super().__init__(
            processor=structlog.processors.JSONRenderer(),
            foreign_pre_chain=build_default_processors(level=level, json_format=True),
        )


class UvicornAccessJSONFormatter(structlog.stdlib.ProcessorFormatter):
    """Access log JSON formatter for Uvicorn with structured logging."""

    def __init__(self, level, *args, **kwargs):
        """Initialize UvicornAccessJSONFormatter."""
        processors = [
            _extract_uvicorn_request_meta,
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            structlog.processors.JSONRenderer(),
        ]

        # pass_foreign_args чтобы прокидывались значения из record.args в positional_args
        super().__init__(
            processors=processors,
            foreign_pre_chain=build_default_processors(level=level, json_format=True),
            pass_foreign_args=True,
        )


class UvicornFileFormatter(structlog.stdlib.ProcessorFormatter):
    """File formatter for Uvicorn logs with structured logging in Logfmt format."""

    def __init__(self, level, *args, **kwargs):
        """Initialize UvicornFileFormatter."""
        super().__init__(
            processor=structlog.processors.LogfmtRenderer(),
            foreign_pre_chain=build_default_processors(level=level, json_format=False),
        )


class UvicornFileJSONFormatter(structlog.stdlib.ProcessorFormatter):
    """File formatter for Uvicorn logs with structured logging in JSON format."""

    def __init__(self, level, *args, **kwargs):
        """Initialize UvicornFileJSONFormatter."""
        super().__init__(
            processor=structlog.processors.JSONRenderer(),
            foreign_pre_chain=build_default_processors(level=level, json_format=True),
        )


def build_uvicorn_log_config(level=logging.INFO, json_console_format: bool = False,
                             json_file_format: bool = True):
    """Build the logging configuration for Uvicorn.

    Args:
        level (int): Logging level.
        json_console_format (bool): Flag to enable JSON formatting for console logs.
        json_file_format (bool): Flag to enable JSON formatting for file logs.

    Returns:
        dict: Uvicorn logging configuration.
    """
    if json_console_format:
        default = UvicornDefaultJSONFormatter
        access = UvicornAccessJSONFormatter
    else:
        default = UvicornDefaultConsoleFormatter  # type: ignore
        access = UvicornAccessConsoleFormatter  # type: ignore

    if json_file_format:
        file_formatter = UvicornFileJSONFormatter
    else:
        file_formatter = UvicornFileFormatter  # type: ignore

    level_name = logging.getLevelName(level)
    return {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                '()': default,
                'level': level,
            },
            'access': {
                '()': access,
                'level': level,
            },
            'file_formatter': {
                '()': file_formatter,
                'level': level,
                'json_format': json_file_format,
            },
        },
        'handlers': {
            'default': {
                'formatter': 'default',
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stdout',
            },
            'access': {
                'formatter': 'access',
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stdout',
            },
            'file': {
                'formatter': 'file_formatter',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': settings.logging.LOG_FILE,
                'backupCount': settings.logging.LOG_BACKUP_COUNT,
                'mode': 'a',
                'encoding': 'utf-8',
            },
        },
        'loggers': {
            'uvicorn': {
                'handlers': ['default', 'file'],
                'level': level_name,
                'propagate': False,
            },
            'uvicorn.error': {
                'level': level_name,
                'handlers': ['default', 'file'],
                'propagate': False,
            },
            'uvicorn.access': {
                'handlers': ['access', 'file'],
                'level': level_name,
                'propagate': False,
            },
        },
    }


def _extract_uvicorn_request_meta(
    wrapped_logger: logging.Logger | None,
    method_name: str,
    event_dict: EventDict,
):
    """Extract metadata from Uvicorn request logs and add them to the event dictionary.

    Args:
        wrapped_logger (Optional[logging.Logger]): Wrapped logger instance.
        method_name (str): Method name.
        event_dict (EventDict): Event dictionary.

    Returns:
        EventDict: Updated event dictionary with request metadata.
    """
    with contextlib.suppress(KeyError, ValueError):
        (
            client_addr,
            method,
            full_path,
            status_code,
        ) = event_dict['positional_args']

        event_dict['client_addr'] = client_addr
        event_dict['http_method'] = method
        event_dict['url'] = full_path
        event_dict['status_code'] = status_code

        event_dict.pop('positional_args')

    return event_dict
