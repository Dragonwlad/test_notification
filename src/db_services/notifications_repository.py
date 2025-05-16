from math import ceil

from fastapi import HTTPException, status
from tortoise.queryset import QuerySet

from src.models.notification import Notification
from src.models.user import User
from tortoise.exceptions import DoesNotExist

from src.rest_models.notification_schema import NotificationCreate, NotificationReadPagination, \
    NotificationRead
from src.rest_models.pagination import Pagination


class NotificationRepository:
    async def create_notification_for_user(
        self,
        user_id: int,
        data: NotificationCreate,
    ) -> Notification:
        user = await User.get(id=user_id)
        return await Notification.create(user=user, **data.dict())

    async def get_user_notifications(
        self,
        user_id: int,
        pagination: Pagination
    ) -> NotificationReadPagination:
        """
        Возвращает пагинированный список уведомлений.
        """
        base_qs: QuerySet = Notification.filter(user_id=user_id)

        total = await base_qs.count()
        page_qs = (
            base_qs
            .offset(pagination.offset or 0)
            .limit(pagination.per_page)
            .order_by("-id" if pagination.order == "desc" else "id")
        )

        notifications = await page_qs

        return NotificationReadPagination(
            total=total,
            count=min(pagination.per_page, total),
            page=pagination.page,
            pages=ceil(total / pagination.per_page),
            items=[NotificationRead.from_orm(n) for n in notifications],
        )

    async def delete_user_notification(self, user_id: int, notification_id: int) -> None:
        try:
            notification = await Notification.get(id=notification_id, user_id=user_id)
            await notification.delete()
        except DoesNotExist:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Notification not found")


notification_repository = NotificationRepository()
