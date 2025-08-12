from bson import ObjectId

def serialize_timekeeping(entry) -> dict:
    return {
        "id": str(entry.get("_id", "")),
        "name": entry.get("name", ""),
        "day": entry.get("day", ""),
        "date": entry.get("date", ""),
        "checkin": entry.get("checkin", ""),
        "checkout": entry.get("checkout", "")
    }

def deserialize_timekeeping_id(timekeeping_id: str) -> ObjectId:
    """Convert string ID to MongoDB ObjectId"""
    try:
        return ObjectId(timekeeping_id)
    except:
        raise ValueError("Invalid timekeeping ID format")
