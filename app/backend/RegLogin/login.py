from app.db.db import User
from app.backend.utils import get_password_hash, create_access_token, authenticate_user, SECRET_KEY, ALGORITHM
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends
from jose import jwt
from app.main.py import app
from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    code: int

@app.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    print(await User.objects.all())
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        return {"code": 401, "access_token": ""}

    token = create_access_token(data = {"email":  user.email})
    user.token = token
    user.save()
    print(jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)['exp'])
    return {"code": 200, "access_token": token}
