import csv
from typing import IO
from core.database import (
    get_database,
    get_employee_collection,
    get_timekeeping_tracking_collection,
    get_employee_train_collection,
    get_timesheet_train_collection

)
from .embedding_service import build_employee_embedding_doc, build_timesheet_embedding_doc

def load_employees_from_csv(file: IO):
    reader = csv.DictReader(file.decode("utf-8").splitlines())
    inserted = 0
    for row in reader:
        name = row.get("Name")
        dob = row.get("Dob")
        team = row.get("Team")
        gender = row.get("Gender")
        if name and dob:
            db = get_database()
            employee_collection = get_employee_collection(db)
            employee_collection.insert_one({"name": name, "dob": dob, "team": team, "gender": gender})

            # Train embeddings for new employee only if not present in employee_train
            train_col = get_employee_train_collection(db)
            exists = train_col.find_one({"name": name, "dob": dob})
            if not exists:
                doc = build_employee_embedding_doc({
                    "name": name,
                    "dob": dob,
                    "team": team,
                    "gender": gender,
                })
                train_col.insert_one(doc)
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
        date = row.get("Date")
        if name and checkin and checkout:
            timekeeping_collection.insert_one({
                "name": name,
                "date": date,
                "checkin": checkin,
                "checkout": checkout
            })
            inserted += 1

            # Train embeddings for new employee only if not present in employee_train
            train_col = get_timesheet_train_collection(db)
            exists = train_col.find_one({"name": name, "date": date})
            if not exists:
                doc = build_timesheet_embedding_doc({
                    "name": name,
                    "date": date,
                    "checkin": checkin,
                    "checkout": checkout,
                })
                train_col.insert_one(doc)
            inserted += 1
    return inserted
