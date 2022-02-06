from datetime import datetime
from tortoise import Model, fields
from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator


class User(Model):
    id = fields.IntField(pk=True, index=True)
    username = fields.CharField(max_length=40, unique=True, null=False)
    email = fields.CharField(max_length=255, unique=True, null=False)
    password = fields.CharField(max_length=128, null=False)
    is_verified = fields.BooleanField(default=False)
    join_date = fields.DatetimeField(default=datetime.utcnow)


class Notification(Model):
    id = fields.IntField(pk=True, index=True)
    description = fields.CharField(max_length=255)
    expiry_date = fields.DateField(nullable=True)
    created_date = fields.DateField(default=datetime.utcnow)


class Picture(Model):
    id = fields.IntField(pk=True, index=True)
    image_path = fields.CharField(max_length=255, null=False, default='default.jpg')
    taken_date = fields.DatetimeField(default=datetime.utcnow)
    taken_by = fields.ForeignKeyField("models.User", related_name="photographer")
    notification = fields.ForeignKeyField("models.Notification", related_name="pictures")


user_pydantic = pydantic_model_creator(User, name="User", exclude=("is_verified",))
user_pydanticIn = pydantic_model_creator(User, name="UserIn", exclude_readonly=True)
user_pydanticOut = pydantic_model_creator(User, name="UserOut", exclude=("password",))

notification_pydantic = pydantic_model_creator(Notification, name="Notification")
notification_pydanticIn = pydantic_model_creator(Notification, name="NotificationIn", exclude_readonly=True)

picture_pydantic = pydantic_model_creator(Picture, name="Picture")
picture_pydanticIn = pydantic_model_creator(Picture, name="PictureIn", exclude_readonly=True)

