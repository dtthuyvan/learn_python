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