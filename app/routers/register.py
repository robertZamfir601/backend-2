from fastapi import Request, APIRouter
from fastapi.responses import HTMLResponse


from jose import jwt
from pydantic import BaseModel

### FAST api security
### Types
from datetime import timedelta
### Register - Login ours
from starlette.responses import JSONResponse, HTMLResponse
from app.backend.utils import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, SECRET_KEY, ALGORITHM, add_token_to_user
## Login Google
from google.oauth2 import id_token
from google.auth.transport import requests
##our files
from ..backend.RegLogin.register import register_or_login_with_google

### login google

### setup
COOKIE_AUTHORIZATION_NAME = "Authorization"
COOKIE_DOMAIN = "localhost"
PROTOCOL = "http://"
FULL_HOST_NAME = "localhost"
PORT_NUMBER = 8000
CLIENT_ID = "829120611572-clp4nv8n5sjhvn7dh1oqq32egp9ef931.apps.googleusercontent.com"
###

router = APIRouter()

### paths 
async def decode(token):
    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)

        # ID token is valid. Get the user's Google Account ID from the decoded token.
        userid = idinfo['sub']
        email = idinfo['email']

        user = await register_or_login_with_google(email, token)
        print("Acas")
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
                    data={"email": email}, expires_delta=access_token_expires)
        print("Almost")
        await add_token_to_user(email, access_token)
        return JSONResponse(content={"status": "200", "message": "Login successfully", "token": access_token})
    except ValueError:
        # Invalid token
        print("E de rau aici")
        return  JSONResponse(content={"status": "400", "message": "You are far away from home"})

class MyToken23(BaseModel):
    token: str


@router.post("/swap_token", response_model=MyToken23)
async def swap_token(item: MyToken23):
    print(item.token)
    res = await decode(item.token)
    return res
###