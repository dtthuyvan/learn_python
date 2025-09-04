def serialize_timekeeping(entry) -> dict:
    return {
        "id": str(entry.get("_id", "")),
        "name": entry.get("name", ""),
        "date": entry.get("date", ""),
        "checkin": entry.get("checkin", ""),
        "checkout": entry.get("checkout", "")
    }
