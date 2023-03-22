from fastapi import Depends, FastAPI
from uvicorn import Config, Server

from .dependencies import get_query_token, get_token_header
from .internal import admin
from .routers import items, users

from .db.db import database, User
from .test.test import add_user

app = FastAPI(dependencies=[Depends(get_query_token)])
##https://testdriven.io/blog/fastapi-docker-traefik/
##https://www.fastapitutorial.com/blog/serving-html-fastapi/
##https://fastapi.tiangolo.com/tutorial/sql-databases/
app.include_router(users.router)
app.include_router(items.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)

@app.get("/")
async def root():
    return await User.objects.all()
    ##return {"message": "Hello Bigger Applications!"}

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