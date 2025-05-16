import os
from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    class Config:
        env_file = os.path.join(os.path.dirname(__file__), '../../.env')
        env_file_encoding = 'utf-8'
        extra = 'ignore'


class ServerSettings(Settings):
    """Model with server settings."""

    __conf_name__ = 'server'

    SERVER_HOST: str = Field(default='0.0.0.0', env='SERVER_HOST')
    SERVER_PORT: int = Field(default='8000', env='SERVER_PORT')
    DEBUG: bool = Field(default=False, env="DEBUG")
    # ALLOW_CREDENTIALS: bool = Field(default=False, env="ALLOW_CREDENTIALS")
    # ALLOW_HEADERS: str = Field(default=False, env="ALLOW_HEADERS")
    # ALLOW_METHODS: str = Field(default=False, env="ALLOW_METHODS")
    # ALLOW_ORIGINS: List[str] = Field(default=False, env="ALLOW_ORIGINS")
    # GUNICORN_WORKERS: int = Field(default=1, env='GUNICORN_WORKERS')
    # GUNICORN_TIMEOUT: int = Field(default=60, env='GUNICORN_TIMEOUT')
    STATIC_FOLDER: Path = Field(default='src/static', env='STATIC_FOLDER')


class LoggingSettings(Settings):
    """Model with logging settings."""

    __conf_name__ = 'logging'

    LOGGING_LEVEL: int = Field(default=10, env='LOGGING_LEVEL')
    LOG_BACKUP_COUNT: int = Field(default=3, env='LOG_BACKUP_COUNT')
    JSON_FILE_FORMAT: bool = Field(default=True, env='JSON_FILE_FORMAT')
    JSON_CONSOLE_FORMAT: bool = Field(default=False, env='JSON_CONSOLE_FORMAT')
    LOG_SIZE: str | int = Field(default='10m', env='LOG_SIZE')
    LOG_FILE: Path = Field(default='logs/logg.log', env='LOG_FILE')
    LOG_FOLDER: Path = Field(default='/', env='LOG_FOLDER')

    def __init__(self, **configuration):
        """Initialize LoggingSettings with logging folder creation."""
        super().__init__(**configuration)
        self.LOG_FOLDER.mkdir(exist_ok=True)

    @field_validator('LOG_SIZE')
    @classmethod
    def _validate_log_size(cls, log_size: str) -> int:
        """Check size format if None.

        Returns:
            int: log size.
        """
        size_types = {
            'b': 1,
            'k': 1024,
            'm': 1024 ** 2,
            'g': 1024 ** 3,
        }
        return int(log_size[:-1]) * size_types[log_size[-1].lower()]


class DatabaseSettings(Settings):
    """Model with db settings."""

    __conf_name__ = 'postgres'

    POSTGRES_USER: str = Field(default='postgres', env='POSTGRES_USER')
    POSTGRES_PASSWORD: str = Field(default='postgres', env='POSTGRES_PASSWORD')
    DB_NAME: str = Field(default='pg', env='DB_NAME')
    DB_HOST: str = Field(default='db', env='DB_HOST')
    DB_PORT: int = Field(default=5432, env='DB_PORT')
    DB_ENGINE: str = Field(default='postgres', env='DB_ENGINE')

    @property
    def DATABASE_URL(self) -> str:

        return (f'{self.DB_ENGINE}://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.DB_HOST}:'
                f'{self.DB_PORT}/{self.DB_NAME}')


class TokenSettings(Settings):
    """Model with auth token settings."""

    __conf_name__ = 'token'

    JWT_SECRET: str = Field(default='JWT_SECRET', env='JWT_SECRET')
    ACCESS_TOKEN_LIFETIME: int = Field(default=3600, env='ACCESS_TOKEN_LIFETIME')
    REFRESH_TOKEN_LIFETIME: int = Field(default=604800, env='ACCESS_TOKEN_LIFETIME')
    ALGORITHM: str = Field(default='HS256', env='ALGORITHM')
    # DATETIME_FORMAT: str


class ProjectSettings(Settings):
    """Model with project settings."""

    db: DatabaseSettings = DatabaseSettings()
    logging: LoggingSettings = LoggingSettings()
    server: ServerSettings = ServerSettings()
    token: TokenSettings = TokenSettings()


settings = ProjectSettings()
