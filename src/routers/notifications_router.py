from fastapi import APIRouter, Depends, status, Query, Path

from src.rest_models.notification_schema import NotificationCreate, NotificationRead

from src.rest_models.notification_schema import NotificationReadPagination
from src.rest_models.pagination import Pagination
from src.routers.deps.pagination import generate_pagination_query_params
from src.services.notification_service import notification_service

from src.routers.deps.auth import get_current_user_id

notifications_router = APIRouter()


@notifications_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_notification(
    payload: NotificationCreate,
    current_user_id: int = Depends(get_current_user_id),
) -> NotificationRead:
    return await notification_service.create(user_id=current_user_id, data=payload)


@notifications_router.get("/")
async def list_notifications(
    pagination: Pagination = Depends(generate_pagination_query_params),
    current_user_id: int = Depends(get_current_user_id),
) -> NotificationReadPagination:
    return await notification_service.list(user_id=current_user_id, pagination=pagination)


@notifications_router.delete("/{notification_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_notification(
    notification_id: int = Path(...),
    current_user_id: int = Depends(get_current_user_id),
):
    await notification_service.delete(user_id=current_user_id, notification_id=notification_id)
