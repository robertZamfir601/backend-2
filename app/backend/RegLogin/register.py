from app.db.db import User
from app.backend.utils import get_password_hash


async def add_user_to_database(email: str, password: str):
    try:
        user = await User.objects.create(email=email, password=get_password_hash(password))
    except:
        user = None
    return user


async def register_or_login_with_google(email: str, token_google: str):
    try:
        user = await User.objects.get_or_create(email=email)
        user = user[0]
    except:
        print("Added user")
    try:
        user.token_google = token_google
        await user.update()
        print("Updated")
    except:
        print("NU am putut updata user")  
