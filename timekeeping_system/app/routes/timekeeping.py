from fastapi import APIRouter, Request, UploadFile, File
from fastapi.templating import Jinja2Templates
from app.core.database import get_database, get_employee_collection, get_timekeeping_tracking_collection
from app.models.timekeeping import serialize_timekeeping
from app.services.csv_loader import load_timekeeping_from_csv
from app.services.ai_gemini_service import make_request
import requests
import httpx
import json

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
    reportDate = "2025-07-26"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "prompt": f"Find employees with full attendance on {reportDate}"
    }

    result_raw = None

    async with httpx.AsyncClient(timeout=120.0) as client:
        try:
            resp = await client.post(url, json=data)
            resp.raise_for_status()
            print(">>>>> Response text:", resp.text)
            print(">>>>> Response content-type:", resp.headers.get("content-type"))
            result_raw = resp.text
        except Exception as e:
            print("Error when get data:", e)
            result_raw = "Couldn't get data from agent."


    return templates.TemplateResponse("full_atendance_report.html", { "request": request, "report_date": reportDate,
        "full_attendance": result_raw})


### This for gender report. Will move to the correct region later
@router.post("/timekeeping/gender_report")
async def make_report_invalid_working_hour1(request: Request, file: UploadFile = File(...)):
    url = "http://127.0.0.1:10000/prompt"
    data = {
        "prompt": "Count the number of male and female employees"
    }

    async with httpx.AsyncClient(timeout=120.0) as client:
        try:
            resp = await client.post(url, json=data)
            resp.raise_for_status()
            print(">>>>> Response text:", resp.text)
            print(">>>>> Response content-type:", resp.headers.get("content-type"))
            result_raw = resp.json()
            if isinstance(result_raw, str):
                result = json.loads(result_raw)
            else:
                result = result_raw
        except httpx.ReadTimeout:
            return templates.TemplateResponse("gender_report.html", {
                "request": request,
                "male_count": 0,
                "female_count": 0,
                "error": "Agent timeout after 120 seconds. Please check the agent backend."
            })
        except Exception as e:
            return templates.TemplateResponse("gender_report.html", {
                "request": request,
                "male_count": 0,
                "female_count": 0,
                "error": f"Connect error agent: {str(e)}"
            })
    
    male = result.get("male_count", 0)
    female = result.get("female_count", 0)
    return templates.TemplateResponse("gender_report.html", {
        "request": request,
        "male_count": male,
        "female_count": female
    })
