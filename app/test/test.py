
from ..db.db import database, User

async def add_user():
    await User.objects.get_or_create(email="bogdan@test.com")
    await User.objects.get_or_create(email="andrei@test.com")