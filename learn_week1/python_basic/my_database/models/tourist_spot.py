from pydantic import BaseModel
from typing import Optional

class TouristSpot(BaseModel):
    id: Optional[str] = "" 
    name: Optional[str] = ""
    sub_title: Optional[str] = ""
    description: Optional[str] = ""
    image: Optional[str] = ""
    price_tour: Optional[str] = ""
    guide_id: Optional[int] = 0
    
    def __str__(self):
        print(F"name {self.name}, description {self.desciption}")