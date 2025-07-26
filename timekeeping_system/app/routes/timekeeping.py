from fastapi import APIRouter, Request, UploadFile, File
from fastapi.templating import Jinja2Templates
from app.core.database import get_database, get_employee_collection, get_timekeeping_tracking_collection
from app.models.timekeeping import serialize_timekeeping
from app.services.csv_loader import load_timekeeping_from_csv
from app.services.ai_gemini_service import make_request
import requests

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/timekeeping")
def list_timekeeping(request: Request):
    db = get_database()
    timekeeping_collection = get_timekeeping_tracking_collection(db)
    data = [serialize_timekeeping(t) for t in timekeeping_collection.find()]
    return templates.TemplateResponse("timekeeping.html", {"request": request, "timekeeping": data})

@router.post("/timekeeping/upload")
async def upload_timekeeping_csv(request: Request, file: UploadFile = File(...)):
    db = get_database()
    timekeeping_collection = get_timekeeping_tracking_collection(db)
    inserted = load_timekeeping_from_csv(await file.read())
    data = [serialize_timekeeping(t) for t in timekeeping_collection.find()]
    message = f"Added {inserted} timekeeping recorded from CSV"
    return templates.TemplateResponse("timekeeping.html", {"request": request, "timekeeping": data, "message": message})

@router.post("/timekeeping/report")
async def make_report_invalid_working_hour(request: Request, file: UploadFile = File(...)):
    url = "http://127.0.0.1:10000/prompt"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "prompt": "Find employees with full attendance on 2025-07-26"
    }

    response = requests.post(url, headers=headers, json=data)
    print("Status code:", response.status_code)
    print("Response JSON:", response.json())
