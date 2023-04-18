from fastapi import Depends, FastAPI, Request, Cookie, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from uvicorn import Config, Server

from jose import jwt
from pydantic import BaseModel
from app.backend.utils import get_user
from ormar import Model, Integer, String, QuerySet
### FAST api security
from fastapi import HTTPException, status, FastAPI, HTTPException, Header
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
### Types
from datetime import datetime, timedelta
from typing import Annotated, Union
### Register - Login ours
from starlette.responses import JSONResponse, HTMLResponse
from .backend.utils import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, authenticate_user, SECRET_KEY, ALGORITHM, add_token_to_user
from .backend.RegLogin.register import add_user_to_database, register_or_login_with_google
## Login Google
from google.oauth2 import id_token
from google.auth.transport import requests
##our files
from .dependencies import get_token_header
from .internal import admin
from .routers import items, users, websites, get_cart
from .db.db import database, User, Website, Product, CartedProd
from .test.test import add_user
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

app = FastAPI()##dependencies=[Depends(get_query_token)]
app.mount("/frontend", StaticFiles(directory="app/frontend/static"), name="static")
templates = Jinja2Templates(directory="./app/frontend/templates")
app.include_router(users.router)
app.include_router(items.router)
app.include_router(websites.router)
app.include_router(get_cart.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

##routes html application
@app.get("/", response_class=HTMLResponse)
async def index_html(request: Request, token: Annotated[str | None, Cookie()] = None):

    if token == None:
        print("no token")
        return templates.TemplateResponse("index.html",{ "request": request })
    else:
        print(jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM))
        data = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        user = await get_user(data["email"])
        print(data["email"])
        if user.token == token:
            return templates.TemplateResponse("index-login.html",{ "request": request })
        else:
            return templates.TemplateResponse("index.html",{ "request": request })

@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html",{ "request": request })


###
@app.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse("register.html",{ "request": request })


@app.post("/register", response_class=HTMLResponse)
async def registerUser(request: Request,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    print("good start")
    user = await User.objects.get_or_none(email=form_data.username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username already taken",
            headers={"WWW-Authenticate": "Bearer"},
        )
    else:   
        user = await add_user_to_database(form_data.username, form_data.password)
    if not user:
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User could not be created",
            headers={"WWW-Authenticate": "Bearer"},
        )
    else:
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"email": user.email}, expires_delta=access_token_expires)
        add_token_to_user(user.email, access_token)
        print(access_token)
        
        return JSONResponse(content={"status": "200", "message": "Registered successfully", "token": access_token})
###


### login google

### setup
COOKIE_AUTHORIZATION_NAME = "Authorization"
COOKIE_DOMAIN = "localhost"
PROTOCOL = "http://"
FULL_HOST_NAME = "localhost"
PORT_NUMBER = 8000
CLIENT_ID = "829120611572-clp4nv8n5sjhvn7dh1oqq32egp9ef931.apps.googleusercontent.com"
###

### paths 
@app.get("/google_login_client", response_class=HTMLResponse)
async def google_login_client(request: Request):
    return templates.TemplateResponse("loginGoogle.html",{ "request": request })

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


@app.post("/swap_token", response_model=MyToken23)
async def swap_token(item: MyToken23):
    print(item.token)
    res = await decode(item.token)
    return res
###

@app.get("/profile", response_class=HTMLResponse, )
async def profile(request: Request, token: Annotated[str | None, Cookie()] = None):
    if token == None:
        return templates.TemplateResponse("index.html",{ "request": request })
    else:
        return templates.TemplateResponse("profile.html",{ "request": request })

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
    await user.update()
    print(jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)['exp'])
    return {"code": 200, "access_token": token}




@app.post("/forms/contact.php")
async def login_for_access_token(email: Annotated[str, Form()], name: Annotated[str, Form()], subject: Annotated[str, Form()], message: Annotated[str, Form()]):
    print("email:" + email)
    print("name:" + name)
    print("subject:" + subject)
    print("message:" + message)


@app.on_event("startup")
async def startup():
    if not database.is_connected:
        await database.connect()
    # create a dummy entry
    await add_user()


@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()


if __name__ == "__main__":  # pragma: no cover
    server = Server(
        Config(
            "runserver:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
        ),
    )

    # do something you want before running the server
    # eg. setting up custom loggers
    server.run()