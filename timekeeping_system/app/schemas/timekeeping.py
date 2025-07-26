from pydantic import BaseModel

class TimeKeepingTracking(BaseModel):
    id: str
    name: str
    day: str
    checkin: str
    checkout: str
