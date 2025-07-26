
def serialize_employee(employee) -> dict:
    return {
        "id": str(employee.get("_id", "")),
        "name": employee.get("name", ""),
        "dob": employee.get("dob", ""),
        "team": employee.get("team", "")
    }
