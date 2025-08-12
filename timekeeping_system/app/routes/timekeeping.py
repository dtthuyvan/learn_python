from fastapi import APIRouter, Request, UploadFile, File, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from core.database import get_database, get_timekeeping_tracking_collection, get_employee_collection, get_timesheet_train_collection
from models.timekeeping import serialize_timekeeping, deserialize_timekeeping_id
from models.employee import serialize_employee
from services.csv_loader import load_timekeeping_from_csv
from services.embedding_service import build_timesheet_embedding_doc
import services.ai_gemini_service as gemini_service
from helper.time_helper import convert_to_12h_format
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

@router.get("/timekeeping/add")
def show_add_timekeeping_form(request: Request):
    db = get_database()
    employee_collection = get_employee_collection(db)
    employees = [serialize_employee(e) for e in employee_collection.find()]
    return templates.TemplateResponse("add_timekeeping.html", {"request": request, "employees": employees})

@router.post("/timekeeping/add")
async def add_timekeeping(
    request: Request,
    employee_name: str = Form(...),
    date: str = Form(...),
    checkin: str = Form(...),
    checkout: str = Form(...)
):
    try:
        db = get_database()
        timekeeping_collection = get_timekeeping_tracking_collection(db)
        checkin_12h = convert_to_12h_format(checkin)
        checkout_12h = convert_to_12h_format(checkout)       
        new_timekeeping = {
            "name": employee_name,
            "date": date,
            "checkin": checkin_12h,
            "checkout": checkout_12h
        }
        
        result = timekeeping_collection.insert_one(new_timekeeping)
        train_col = get_timesheet_train_collection(db)
        doc = build_timesheet_embedding_doc(new_timekeeping)
        result = train_col.insert_one(doc)

        data = [serialize_timekeeping(t) for t in timekeeping_collection.find()]
        time_format = "%I:%M %p"
        for item in data:
            try:
                checkin_time = datetime.strptime(item['checkin'], time_format)
                checkout_time = datetime.strptime(item['checkout'], time_format)
                duration = checkout_time - checkin_time
                hours = duration.total_seconds() / 3600
                item['duration'] = round(hours, 2)
            except ValueError:
                item['duration'] = "N/A"
        
        message = f"Timekeeping record for '{employee_name}' on {date} added successfully!"
        return templates.TemplateResponse("timekeeping.html", {
            "request": request, 
            "timekeeping": data, 
            "message": message
        })
        
    except Exception as e:
        error_message = f"Error adding timekeeping: {str(e)}"
        db = get_database()
        employee_collection = get_employee_collection(db)
        employees = [serialize_employee(e) for e in employee_collection.find()]
        return templates.TemplateResponse("add_timekeeping.html", {
            "request": request, 
            "error": error_message,
            "employees": employees
        })

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

@router.delete("/timekeeping/{timekeeping_id}")
async def delete_timekeeping(timekeeping_id: str):
    try:
        # Validate and convert timekeeping_id to ObjectId
        try:
            object_id = deserialize_timekeeping_id(timekeeping_id)
        except ValueError:
            return JSONResponse(
                status_code=400,
                content={"success": False, "message": "Invalid timekeeping ID format"}
            )
        
        db = get_database()
        timekeeping_collection = get_timekeeping_tracking_collection(db)
        
        # Check if timekeeping record exists before deleting
        existing_record = timekeeping_collection.find_one({"_id": object_id})
        if not existing_record:
            return JSONResponse(
                status_code=404,
                content={"success": False, "message": "Timekeeping record not found"}
            )
        
        # Delete timekeeping record from main collection
        result = timekeeping_collection.delete_one({"_id": object_id})
        
        if result.deleted_count > 0:
            return JSONResponse(
                status_code=200,
                content={"success": True, "message": f"Timekeeping record for '{existing_record.get('name', '')}' on {existing_record.get('date', '')} deleted successfully"}
            )
        else:
            return JSONResponse(
                status_code=500,
                content={"success": False, "message": "Failed to delete timekeeping record"}
            )
            
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": f"Error deleting timekeeping record: {str(e)}"}
        )
