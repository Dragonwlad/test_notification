from tortoise import models, fields
from enum import Enum


class NotificationType(str, Enum):
    like = "like"
    comment = "comment"
    repost = "repost"


class Notification(models.Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="notifications")
    type = fields.CharEnumField(NotificationType)
    text = fields.CharField(max_length=255)
    created_at = fields.DatetimeField(auto_now_add=True)
