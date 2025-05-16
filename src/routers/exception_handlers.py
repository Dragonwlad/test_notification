"""Модуль с обработчиками исключений."""
import structlog
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse


from src.exceptions import  UnexpectedError


logger = structlog.stdlib.get_logger('post')


async def unexpected_error(
    request: Request,
    exc: UnexpectedError,
) -> JSONResponse:
    """Handle UnexpectedError.

    Args:
        request (Request): The incoming request.
        exc (UnexpectedError): The exception instance.

    Returns:
        JSONResponse: A JSON response with the error message and status code.
    """
    logger.warning('Неизвестная ошибка: {error}.'.format(error=str(exc.error)))
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'success': False, 'error': str(exc.error)},
    )


exception_handlers: dict = {
    UnexpectedError: unexpected_error,
}
