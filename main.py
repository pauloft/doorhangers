import os
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from app.models import User, user_pydantic, user_pydanticIn, user_pydanticOut
from app.models import Notification, notification_pydantic, notification_pydanticIn
from app.models import Picture, picture_pydantic, picture_pydanticIn
from dotenv import load_dotenv


load_dotenv()
app = FastAPI()


@app.get("/")
def greet():
    return {"Hello": "There World!"}

@app.get("/users")
async def get_all_users():
    """Get all users from the database"""
    return await user_pydantic.from_queryset(User.all())

@app.post("/user")
async def add_one_user(user_info: user_pydanticIn):
    """Add one new user to the database"""
    user_obj = await User.create(**user_info.dict(exclude_unset=True))
    response = await user_pydantic.from_tortoise_orm(user_obj)
    return {"status": "OK", "data": response}

@app.get("/user/{user_id}")
async def get_specific_user(user_id: int):
    """Fetch a specific user by the user id"""
    response = await user_pydantic.from_queryset_single(User.get(id=user_id))
    return {"status": "OK", "data": response}

@app.put("/user/{user_id}")
async def update_user(user_id: int, user_info: user_pydanticIn):
    user = await User.get(id=user_id)
    user_info = user_info.dict(exclude_unset=True)
    user.username = user_info["username"]
    user.email = user_info["email"]
    user.password = user_info["password"]
    user.is_verified = user_info["is_verified"]
    await user.save()
    response = await user_pydantic.from_tortoise_orm(user)
    return {"status": "OK", "data": response}

@app.delete("/user/{user_id")
async def delete_user(user_id: int):
    await User.get(id=user_id).delete()
    return {"status": "ok"}

register_tortoise(
    app,
    db_url="postgres://{}:{}@{}:{}/{}".format(
        os.getenv("db_user"),
        os.getenv("db_pass"),
        os.getenv("db_host", "localhost"),
        os.getenv("db_port"),
        os.getenv("db_name")
    ),
    modules={"models": ["app.models"]},
    generate_schemas=True,
    add_exception_handlers=True
)