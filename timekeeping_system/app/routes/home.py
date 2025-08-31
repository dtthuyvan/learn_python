from fastapi import APIRouter, Request, UploadFile, File, Form
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/")
def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/home")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

