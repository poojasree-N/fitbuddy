from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

from app.routes import router
from app.database import Base, engine
from app import models

app = FastAPI()

templates = Jinja2Templates(directory="templates")

Base.metadata.create_all(bind=engine)

app.include_router(router)


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )