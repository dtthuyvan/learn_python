from pydantic import BaseModel

class Employee(BaseModel):
    id: str
    name: str
    dob: str
    team: str
