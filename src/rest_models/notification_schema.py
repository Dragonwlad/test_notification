from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field
from tortoise.contrib.pydantic import pydantic_model_creator
from src.models.notification import Notification, NotificationType
from src.models.user import User
from src.rest_models.base_schema import BaseSchema
from src.rest_models.pagination import PaginationOut


class NotificationCreate(BaseModel):
    """
    Входная модель для создания уведомления.
    """
    type: NotificationType
    text: str = Field(..., max_length=255)


class NotificationRead(BaseSchema):
    """
    Входная модель для создания уведомления.
    """
    id: int
    type: str
    text: str
    created_at: datetime
    user_id: int


class NotificationReadPagination(PaginationOut):
    """Model with client pagination schema out."""

    items: list[NotificationRead]
