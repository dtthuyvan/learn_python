import os
from dotenv import load_dotenv
from pymongo import MongoClient


_cached_client = None
_cached_db = None


def get_database():
    global _cached_client, _cached_db
    if _cached_db is not None:
        return _cached_db

    load_dotenv()
    connection_string = os.getenv("MONGO_CONNECTION_STRING")
    database_name = os.getenv("MONGO_DB_NAME", "timekeeping")

    if not connection_string:
        raise ValueError("Please set MONGO_CONNECTION_STRING in the environment or .env file")

    _cached_client = MongoClient(connection_string)
    _cached_db = _cached_client[database_name]
    return _cached_db


def get_collection(collection_name: str):
    db = get_database()
    return db[collection_name]


