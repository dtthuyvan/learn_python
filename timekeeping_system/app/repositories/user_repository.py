from typing import Optional
from bson import ObjectId
from app.schemas.user import UserCreate
from app.core.security import hash_password


class UserRepository:
    def __init__(self, db):
        # db is a pymongo database instance
        self.db = db
        self.col = db["users"]

    def create_user(self, user: UserCreate) -> dict:
        doc = {
            "username": user.username,
            "email": user.email,
            "hashed_password": hash_password(user.password),
        }
        res = self.col.insert_one(doc)
        doc["_id"] = res.inserted_id
        return doc

    def get_user_by_username(self, username: str) -> Optional[dict]:
        return self.col.find_one({"username": username})

    def get_user_by_email(self, email: str) -> Optional[dict]:
        return self.col.find_one({"email": email})

    def get_user(self, user_id: str) -> Optional[dict]:
        try:
            oid = ObjectId(user_id)
        except Exception:
            return None
        return self.col.find_one({"_id": oid})
