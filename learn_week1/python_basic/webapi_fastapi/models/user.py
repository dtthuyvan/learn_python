from pydantic import BaseModel

# Define request body
class User(BaseModel):
    name: str
    age: int