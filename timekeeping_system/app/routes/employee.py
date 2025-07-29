from fastapi import APIRouter, Request, UploadFile, File, Form
from fastapi.templating import Jinja2Templates
from app.core.database import get_database, get_employee_collection, get_timekeeping_tracking_collection
from app.models.employee import serialize_employee
from app.services.csv_loader import load_employees_from_csv, load_timekeeping_from_csv
router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
import httpx
import json

@router.get("/employees")
def list_employees(request: Request):
    db = get_database()
    employee_collection = get_employee_collection(db)
    employees = [serialize_employee(e) for e in employee_collection.find()]
    return templates.TemplateResponse("employees.html", {"request": request, "employees": employees})


@router.post("/employees/upload")
async def upload_csv(request: Request, file: UploadFile = File(...)):
    inserted = load_employees_from_csv(await file.read())
    db = get_database()
    employee_collection = get_employee_collection(db)
    employees = [serialize_employee(e) for e in employee_collection.find()]
    message = f"Added {inserted} new employee from CSV"
    return templates.TemplateResponse("employees.html", {"request": request, "employees": employees, "message": message})


@router.post("/employees/report")
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