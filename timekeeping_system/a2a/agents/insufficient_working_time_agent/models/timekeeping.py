def serialize_timekeeping(entry) -> dict:
    return {
        "id": str(entry.get("_id", "")),
        "name": entry.get("name", ""),
        "day": entry.get("day", ""),
        "checkin": entry.get("checkin", ""),
        "checkout": entry.get("checkout", "")
    }
