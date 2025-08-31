import sys
import os
from dotenv import load_dotenv
from pymongo import MongoClient

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def get_database():
    load_dotenv()
    connection = os.getenv("MONGO_CONNECTION_STRING")
    database_name = os.getenv("MONGO_DB_NAME", "timekeeping")

    if not connection:
        raise ValueError("Please setup database connection string!")

    myclient = MongoClient(connection)
    mydb = myclient[database_name]
    return mydb


def get_employee_collection(mydb):
    mycol = mydb["x_employee_train"]
    return mycol


def get_timekeeping_tracking_collection(mydb):
    mycol = mydb["x_timesheet_train"]
    return mycol


def get_x_employee_train_collection(mydb):
    mycol = mydb["x_employee_train"]
    return mycol


def get_x_timesheet_train_collection(mydb):
    mycol = mydb["x_timesheet_train"]
    return mycol


if __name__ == "__main__":
    pass
