from tortoise import models, fields


class User(models.Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50, unique=True)
    avatar_url = fields.CharField(max_length=255, default="https://example.com/avatar.png")
    password = fields.CharField(max_length=128)
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return self.username
