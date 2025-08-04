from fastapi import APIRouter, Request, UploadFile, File
from fastapi.templating import Jinja2Templates
from core.database import get_database, get_timekeeping_tracking_collection, get_employee_collection
from models.timekeeping import serialize_timekeeping
from models.employee import serialize_employee
from services.csv_loader import load_timekeeping_from_csv
import services.ai_gemini_service as gemini_service
import requests
from datetime import datetime

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/timekeeping")
def list_timekeeping(request: Request):
    db = get_database()
    timekeeping_collection = get_timekeeping_tracking_collection(db)
    data = [serialize_timekeeping(t) for t in timekeeping_collection.find()]
    time_format = "%I:%M %p"
    #print(data)
    for item in data:
        checkin_time = datetime.strptime(item['checkin'], time_format)
        checkout_time = datetime.strptime(item['checkout'], time_format)
        duration = checkout_time - checkin_time
        hours = duration.total_seconds() / 3600
        item['duration'] = round(hours, 2) 
        #print(item['duration'])
    return templates.TemplateResponse("timekeeping.html", {"request": request, "timekeeping": data})

@router.post("/timekeeping/upload")
async def upload_timekeeping_csv(request: Request, file: UploadFile = File(...)):
    db = get_database()
    timekeeping_collection = get_timekeeping_tracking_collection(db)
    inserted = load_timekeeping_from_csv(await file.read())
    data = [serialize_timekeeping(t) for t in timekeeping_collection.find()]
    time_format = "%I:%M %p"
    for item in data:
        checkin_time = datetime.strptime(item['checkin'], time_format)
        checkout_time = datetime.strptime(item['checkout'], time_format)
        duration = checkout_time - checkin_time
        hours = duration.total_seconds() / 3600
        item['duration'] = round(hours, 2) 

    message = f"Added {inserted} timekeeping recorded from CSV"
    return templates.TemplateResponse("timekeeping.html", {"request": request, "timekeeping": data, "message": message})

@router.get("/timekeeping/insufficient-report")
async def make_insufficient_working_hour_report(request: Request):
    db = get_database()
    timekeeping_collection = get_timekeeping_tracking_collection(db)
    data = [serialize_timekeeping(t) for t in timekeeping_collection.find()]
    for item in data:
        item.pop('id', None)
    result = gemini_service.analyze_report_insufficient(data)
    message="Analyzing and reporting have just done!"
    return templates.TemplateResponse("timekeeping.html", 
                                      {"request": request, "timekeeping": None, "message": message, "report_msg": result, "report_title": "⚠️ Employees with Insufficient Working Hours"})

@router.get("/timekeeping/full-hour-report")
async def make_full_time_report(request: Request):
    db = get_database()
    timekeeping_collection = get_timekeeping_tracking_collection(db)
    data = [serialize_timekeeping(t) for t in timekeeping_collection.find()]
    for item in data:
        item.pop('id', None)
    
    employee_collection = get_employee_collection(db)
    employees = [serialize_employee(e) for e in employee_collection.find()]
    emp_names = [item['name'] for item in employees]
    name_str = ', '.join(emp_names)

    result = gemini_service.analyze_full_time_report(data, name_str)
    message="Analyzing and reporting have just done!"
    return templates.TemplateResponse("timekeeping.html", 
                                      {"request": request, "timekeeping": None, "message": message, "report_msg": result, "report_title": "📊 Employees work full time all days"})

@router.get("/timekeeping/full-attendance-report")
async def make_full_attendance_report(request: Request):
    db = get_database()
    timekeeping_collection = get_timekeeping_tracking_collection(db)
    data = [serialize_timekeeping(t) for t in timekeeping_collection.find()]
    for item in data:
        item.pop('id', None)

    result = gemini_service.analyze_full_attendance_report(data)
    message="Analyzing and reporting have just done!"
    return templates.TemplateResponse("timekeeping.html", 
                                      {"request": request, "timekeeping": None, "message": message, "report_msg": result, "report_title": "📊 Employees have full attendance report"})
