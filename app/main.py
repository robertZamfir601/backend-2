from fastapi import Depends, FastAPI
from fastapi.templating import Jinja2Templates

from dependencies import get_query_token, get_token_header
from internal import admin
from routers import items, users

app = FastAPI(dependencies=[Depends(get_query_token)])
app.mount("frontend/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="frontend/templates")
app.include_router(users.router)
app.include_router(items.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)

##https://testdriven.io/blog/fastapi-docker-traefik/
##https://www.fastapitutorial.com/blog/serving-html-fastapi/
##https://fastapi.tiangolo.com/tutorial/sql-databases/

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}

@app.get("/login", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse("login.html")