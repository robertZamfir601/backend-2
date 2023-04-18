


from datetime import datetime, timedelta
from pydantic import BaseModel

from typing import Annotated, Union
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError, jwt

from ..db.db import User

SECRET_KEY = "7bca70d8d8891edc6f2388775a09e7bb9b9175d114b467a1d8226b57befde103"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

### Models for Login - Register
class Token(BaseModel):
   access_token: str
   token_type: str

class LoginPostBody(BaseModel):     
   name: str   
   password: str


class TokenData(BaseModel):
   username: Union[str, None] = None
###


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    print(hashed_password)
    return pwd_context.verify(plain_password, hashed_password)


async def get_user(username: str):
    try:
        user = await User.objects.get(email=username)
    except:
        user =  None
    return user



async def authenticate_user(username: str, password: str):
    user = await get_user(username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def add_token_to_user(email: str, token: str):
    try:
        user = await User.objects.get(email=email)
        user.token = token
        await user.update()
        print("Updated token")
    except:
        print("Can't update token for inexistent user")
        user = None