from app.db.db import User
from app.backend.utils import get_password_hash


async def add_user_to_database(email: str, password: str):
    try:
        user = await User.objects.create(email=email, password=get_password_hash(password))
    except:
        user = None
    return user