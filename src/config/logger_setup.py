"""Модуль для настройки structlog.

Этот модуль предоставляет функции для настройки журнала с помощью structlog,
включая настройки для ведения консоли и файлов,
и различные процессоры для форматирования и обогащения сообщений журнала.
"""

import logging
import logging.handlers as logging_handlers
import sys
import os

import structlog
from structlog.types import EventDict, Processor

from src.config.settings import settings


def configure_logger(
    level=logging.DEBUG,
    json_console_format: bool = False,
    json_file_format: bool = True,
):
    """Настройте регистратор с указанными настройками.

    Args:
        level (int): Logging level.
        json_console_format (bool): Flag to enable JSON formatting for console logs.
        json_file_format (bool): Flag to enable JSON formatting for file logs.
    """
    _configure_structlog(level=level, json_format=json_console_format)
    _configure_default_file_logging(level=level, json_format=json_file_format)
    _configure_default_console_logging(level=level, json_format=json_console_format)


def build_default_processors(level: int, json_format: bool):
    """Build the default processors for structlog.

    Args:
        level (int): Logging level.
        json_format (bool): Flag to enable JSON formatting.

    Returns:
        List[Processor]: List of structlog processors.
    """
    callsite_parameters = {
        structlog.processors.CallsiteParameter.MODULE,
        structlog.processors.CallsiteParameter.FILENAME,
        structlog.processors.CallsiteParameter.FUNC_NAME,
        structlog.processors.CallsiteParameter.PROCESS_NAME,
        structlog.processors.CallsiteParameter.THREAD_NAME,
    }
    callsite_debug_parameters = {
        structlog.processors.CallsiteParameter.PATHNAME,
        structlog.processors.CallsiteParameter.THREAD,
        structlog.processors.CallsiteParameter.PROCESS,
    }
    if level == logging.DEBUG:
        callsite_parameters.update(callsite_debug_parameters)
    shared_processors: list[Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.CallsiteParameterAdder(callsite_parameters),
        _drop_color_message_key,
        structlog.processors.TimeStamper(fmt='iso'),
        structlog.processors.StackInfoRenderer(),
    ]
    if json_format:
        shared_processors.append(structlog.processors.format_exc_info)

    return shared_processors


def _drop_color_message_key(_, __, event_dict: EventDict) -> EventDict:
    """Drop the 'color_message' key from the event dictionary if it exists.

    Args:
        event_dict (EventDict): Event dictionary.

    Returns:
        EventDict: Updated event dictionary.
    """
    event_dict.pop('color_message', None)
    return event_dict


def _configure_structlog(*, level, json_format):
    """Configure structlog with the specified settings.

    Args:
        level (int): Logging level.
        json_format (bool): Flag to enable JSON formatting.
    """
    structlog.configure_once(
        processors=build_default_processors(level, json_format)
                   + [
                       # used for integration with default logging
                       structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
                   ],
        logger_factory=structlog.stdlib.LoggerFactory(),
    )


def _configure_default_file_logging(*, level, json_format) -> None:
    """Configure default file logging with the specified settings.

    Args:
        level (int): Logging level.
        json_format (bool): Flag to enable JSON formatting.
    """
    if json_format:
        log_renderer = structlog.processors.JSONRenderer()
    else:
        log_renderer = structlog.processors.LogfmtRenderer()  # type: ignore

    shared_processors = build_default_processors(level, json_format)
    formatter = structlog.stdlib.ProcessorFormatter(
        foreign_pre_chain=shared_processors,
        processors=[
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            log_renderer,
        ],
    )

    log_path = settings.logging.LOG_FILE
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    file_handler = logging_handlers.RotatingFileHandler(
        filename=log_path,
        maxBytes=settings.logging.LOG_SIZE,
        backupCount=settings.logging.LOG_BACKUP_COUNT,
        mode='a',
        encoding='utf-8',
    )

    file_handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.addHandler(file_handler)
    root_logger.setLevel(settings.logging.LOGGING_LEVEL)


def _configure_default_console_logging(*, level, json_format: bool):
    """Configure default console logging with the specified settings.

    Args:
        level (int): Logging level.
        json_format (bool): Flag to enable JSON formatting.
    """
    renderer_processor = (
        structlog.processors.JSONRenderer()
        if json_format
        else structlog.dev.ConsoleRenderer()
    )

    formatter = structlog.stdlib.ProcessorFormatter(
        processors=build_default_processors(level, json_format)
                   + [
                       structlog.stdlib.ProcessorFormatter.remove_processors_meta,
                       renderer_processor,
                   ],
    )

    stream_handler = logging.StreamHandler(stream=sys.stdout)
    stream_handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.addHandler(stream_handler)
    root_logger.setLevel(level)
