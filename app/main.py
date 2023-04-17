from fastapi import Depends, FastAPI, Request, Cookie
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
from .backend.utils import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, authenticate_user, SECRET_KEY, ALGORITHM
from .backend.RegLogin.register import add_user_to_database
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
        data={"sub": user.email}, expires_delta=access_token_expires)
        print(access_token)
        return templates.TemplateResponse("profile.html",{ "request": request })
###


@app.get("/profile", response_class=HTMLResponse)
async def profile(request: Request):
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