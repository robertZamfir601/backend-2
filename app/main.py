from fastapi import Depends, FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from uvicorn import Config, Server

### FAST api security
from fastapi import HTTPException, status, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
###


### Types

from datetime import datetime, timedelta
from typing import Annotated, Union
###


### Register - Login ours
from .backend.utils import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from .backend.RegLogin.register import add_user_to_database

###


##our files
from .dependencies import get_token_header
from .internal import admin
from .routers import items, users
from .db.db import database, User, Website, Product, CartedProd
from .test.test import add_user

app = FastAPI()##dependencies=[Depends(get_query_token)]
app.mount("/frontend", StaticFiles(directory="app/frontend/static"), name="static")
templates = Jinja2Templates(directory="./app/frontend/templates")
app.include_router(users.router)
app.include_router(items.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)


##routes html application
@app.get("/", response_class=HTMLResponse)
async def index_html(request: Request):
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
