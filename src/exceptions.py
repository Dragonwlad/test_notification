"""Module with exception classes."""
from starlette.requests import ClientDisconnect


class UnexpectedError(Exception):
    """Исключение вызывается при необработанной ошибке."""

    def __init__(
        self,
        request_data: str | None = None,
        error: str | None = None,
    ):
        """Initialize UnexpectedError.

        Args:
            request_data (str): Тело запроса,
            error (str): Текст ошибки.
        """
        self.request_data = request_data
        self.error = error
