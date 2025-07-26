import csv
from typing import IO
from app.core.database import get_database, get_employee_collection, get_timekeeping_tracking_collection

def load_employees_from_csv(file: IO):
    reader = csv.DictReader(file.decode("utf-8").splitlines())
    inserted = 0
    for row in reader:
        name = row.get("Name")
        dob = row.get("Dob")
        team = row.get("Team")
        if name and dob:
            db = get_database()
            employee_collection = get_employee_collection(db)
            employee_collection.insert_one({"name": name, "dob": dob, "team": team})
            inserted += 1
    return inserted

def load_timekeeping_from_csv(file: IO):
    reader = csv.DictReader(file.decode("utf-8").splitlines())
    inserted = 0
    for row in reader:
        db = get_database()
        timekeeping_collection = get_timekeeping_tracking_collection(db)
        name = row.get("Name")
        checkin = row.get("CheckInTime")
        checkout = row.get("CheckOutTime")
        day = row.get("Day")
        if name and checkin and checkout:
            timekeeping_collection.insert_one({
                "name": name,
                "day": day,
                "checkin": checkin,
                "checkout": checkout
            })
            inserted += 1
    return inserted
