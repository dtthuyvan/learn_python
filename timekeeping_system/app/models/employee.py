from bson import ObjectId

def serialize_employee(employee) -> dict:
    return {
        "id": str(employee.get("_id", "")),
        "name": employee.get("name", ""),
        "dob": employee.get("dob", ""),
        "team": employee.get("team", ""),
        "gender": employee.get("gender", "")
    }

def deserialize_employee_id(employee_id: str) -> ObjectId:
    """Convert string ID to MongoDB ObjectId"""
    try:
        return ObjectId(employee_id)
    except:
        raise ValueError("Invalid employee ID format")
