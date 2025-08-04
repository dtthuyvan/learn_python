from fastapi import APIRouter, Request, UploadFile, File, Form
from fastapi.templating import Jinja2Templates
from core.database import get_database, get_employee_collection, get_timekeeping_tracking_collection
from models.employee import serialize_employee
from services.csv_loader import load_employees_from_csv, load_timekeeping_from_csv
import services.ai_gemini_service as gemini_service

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

@router.get("/employees/gender-report")
async def make_gender_report(request: Request):
    db = get_database()
    employee_collection = get_employee_collection(db)
    data = [serialize_employee(t) for t in employee_collection.find()]
    for item in data:
        item.pop('id', None)
        item.pop('dob', None)
        item.pop('team', None)
    result = gemini_service.analyze_gender_report(data)
    message="Analyzing and reporting have just done!"
    return templates.TemplateResponse("employees.html", 
                                      {"request": request, "message": message, "report_msg": result, "report_title": "Gender Report"})
