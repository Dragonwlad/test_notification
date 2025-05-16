import structlog

from src.rest_models.notification_schema import NotificationCreate
from src.db_services.notifications_repository import notification_repository
from src.rest_models.notification_schema import NotificationRead

from src.rest_models.notification_schema import NotificationReadPagination
from src.rest_models.pagination import Pagination
from src.services.base_service import BaseService


logger = structlog.stdlib.get_logger('notification_service')


class NotificationService(BaseService):

    async def create(self, user_id: int, data: NotificationCreate):
        obj = await self.db.create_notification_for_user(user_id=user_id, data=data)
        return NotificationRead.from_orm(obj)

    async def list(self, user_id: int, pagination: Pagination) -> NotificationReadPagination:
        result = await self.db.get_user_notifications(
            user_id=user_id,
            pagination=pagination
        )
        return result

    async def delete(self, user_id: int, notification_id: int):
        await self.db.delete_user_notification(user_id=user_id, notification_id=notification_id)


notification_service = NotificationService(db=notification_repository)
