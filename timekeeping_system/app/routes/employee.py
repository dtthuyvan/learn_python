from fastapi import APIRouter, Request, UploadFile, File, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from core.database import get_database, get_employee_collection, get_timekeeping_tracking_collection
from models.employee import serialize_employee, deserialize_employee_id
from services.csv_loader import load_employees_from_csv, get_employee_train_collection
import services.ai_gemini_service as gemini_service
from services.embedding_service import build_employee_embedding_doc

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/employees")
def list_employees(request: Request):
    db = get_database()
    employee_collection = get_employee_collection(db)
    employees = [serialize_employee(e) for e in employee_collection.find()]
    return templates.TemplateResponse("employees.html", {"request": request, "employees": employees})

@router.get("/employees/add")
def show_add_employee_form(request: Request):
    return templates.TemplateResponse("add_employee.html", {"request": request})

@router.post("/employees/add")
async def add_employee(
    request: Request,
    name: str = Form(...),
    gender: str = Form(...),
    dob: str = Form(...),
    team: str = Form(...)
):
    try:
        db = get_database()
        employee_collection = get_employee_collection(db)
        
        new_employee = {
            "name": name,
            "gender": gender,
            "dob": dob,
            "team": team
        }
        
        inserted = 0
        exists = train_col.find_one({"name": name})
        if not exists:
            result = employee_collection.insert_one(new_employee)
            inserted += 1
        
        train_col = get_employee_train_collection(db)
        exists = train_col.find_one({"name": name})
        if not exists:
            doc = build_employee_embedding_doc(new_employee)
            train_col.insert_one(doc)
            inserted += 1
        
        if inserted == 0: 
            message = f"Employee {name} existed"
        else:
            message = f"Employee '{name}' added successfully!"
        employees = [serialize_employee(e) for e in employee_collection.find()]
        return templates.TemplateResponse("employees.html", {
            "request": request, 
            "employees": employees, 
            "message": message
        })
        
    except Exception as e:
        error_message = f"Error adding employee: {str(e)}"
        return templates.TemplateResponse("add_employee.html", {
            "request": request, 
            "error": error_message
        })

@router.delete("/employees/{employee_id}")
async def delete_employee(employee_id: str):
    try:
        # Validate and convert employee_id to ObjectId
        try:
            object_id = deserialize_employee_id(employee_id)
        except ValueError:
            return JSONResponse(
                status_code=400,
                content={"success": False, "message": "Invalid employee ID format"}
            )
        
        db = get_database()
        employee_collection = get_employee_collection(db)
        
        # Check if employee exists before deleting
        existing_employee = employee_collection.find_one({"_id": object_id})
        if not existing_employee:
            return JSONResponse(
                status_code=404,
                content={"success": False, "message": "Employee not found"}
            )
        
        # Delete employee from main collection
        result = employee_collection.delete_one({"_id": object_id})
        
        if result.deleted_count > 0:
            # Delete from training collection if exists
            try:
                train_col = get_employee_train_collection(db)
                train_col.delete_many({"name": existing_employee.get("name", "")})
            except Exception as train_error:
                # Log training deletion error but don't fail the main deletion
                print(f"Warning: Could not delete from training collection: {train_error}")
            
            return JSONResponse(
                status_code=200,
                content={"success": True, "message": f"Employee '{existing_employee.get('name', '')}' deleted successfully"}
            )
        else:
            return JSONResponse(
                status_code=500,
                content={"success": False, "message": "Failed to delete employee"}
            )
            
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": f"Error deleting employee: {str(e)}"}
        )


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
