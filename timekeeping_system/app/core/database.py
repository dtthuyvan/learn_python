import sys
import os
from dotenv import load_dotenv
from pymongo import MongoClient

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def get_database():
    load_dotenv()
    connection = os.getenv("MONGO_CONNECTION_STRING")

    if not connection:
        raise ValueError("Please setup database connection string!")

    myclient = MongoClient(connection)
    mydb = myclient[
        "timekeeping"
    ]  # In MongoDB, a database is not created until it gets content!
    return mydb


def get_employee_collection(mydb):
    mycol = mydb["employee_train"]
    return mycol


def get_timekeeping_tracking_collection(mydb):
    mycol = mydb["timesheet_train"]
    return mycol


def get_employee_train_collection(mydb):
    mycol = mydb["employee_train"]
    return mycol


def get_timesheet_train_collection(mydb):
    mycol = mydb["timesheet_train"]
    return mycol


if __name__ == "__main__":
    pass
