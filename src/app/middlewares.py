"""Module with app middlewares."""
import json
import time
import uuid

import structlog
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import ClientDisconnect

logger = structlog.stdlib.get_logger('middleware')


def base_http_middleware(app):
    return BaseHTTPMiddleware(app)


async def logging_middleware(request: Request, call_next) -> Response:
    """
    Промежуточное программное обеспечение для добавления контекста запроса.

    Args:
        request (Request): Входящий HTTP -запрос.
        call_next (Callable): The next middleware or route handler to call.

    Returns:
        Response: FastAPI response object.
    """

    request_id = request.headers.get('request-id', uuid.uuid4().hex[:8])
    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(request_id=request_id)

    try:
        body = await request.body()
        try:
            parsed_body = json.loads(body)
        except json.JSONDecodeError:
            parsed_body = body.decode("utf-8") if body else None
    except ClientDisconnect:
        logger.warning("Клиент отключен в связи с долгим ожиданием")
        parsed_body = None

    logger.info('[Request] Path: {path}. Body: {body}'.format(
        path=request.url.path,
        body=parsed_body,
        )
    )

    response: Response = await call_next(request)
    return response


async def process_time_header_middleware(request: Request, call_next) -> Response:
    """Добавляет лог с расчетом времени ответа.

    Args:
        request (Request): Входящий HTTP -запрос.
        call_next (Callable): Следующий промежуточный обработчик или
        обработчик маршрута, для вызова.

    Returns:
        Response: HTTP - ответ.
    """
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time

    logger.info('[Request] Path: {path}. Process-Time: {pt}'.format(
        path=request.url.path,
        pt=str(process_time)
    ))
    return response

