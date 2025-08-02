from fastapi import APIRouter, Request, UploadFile, File
from fastapi.templating import Jinja2Templates
from app.core.database import get_database, get_timekeeping_tracking_collection
from app.models.timekeeping import serialize_timekeeping
from app.services.csv_loader import load_timekeeping_from_csv

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