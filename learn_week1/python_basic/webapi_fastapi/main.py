from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from .models.user import User
from bson import ObjectId
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from my_database.my_db import get_database, get_tour_guid, get_tourist_spot
from my_database.convert_data import convert_list_objectid_to_str as convert_data
from my_database.convert_data import convert_obj_objectid_to_str as convert_obj
from my_database.models.tourist_spot import TouristSpot

templates = Jinja2Templates(directory="templates")
app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Welcome to FastAPI!"}

@app.get("/hello", response_class=HTMLResponse)
async def hello():
    return "<h1>Hello from FastAPI Web!</h1>"

@app.get("/greet")
async def greet(request: Request, name: str = "Van"):
    return templates.TemplateResponse("hello.html", {"request": request, "name": name})

# POST method
@app.post("/users/create")
async def create_user(user: User):
    return {
        "message": f"User {user.name} (age {user.age}) created successfully."
    }

@app.get("/tourist-spot")
async def get_tourist_spots():
    mydb = get_database()
    cusor = get_tourist_spot(mydb)
    data = list(cusor)
    data = convert_data(data)
    return {
        "message": "success",
        "data": data
    }

@app.get("/tourist-spot/detail/{id}")
async def get_tourist_detail(id):
    mydb = get_database()
    mycol = mydb["tourist_spot"]
    my_query = {"_id": ObjectId(id)}
    data = mycol.find_one(my_query)
    data = convert_obj(data)
    return {
        "message": "success",
        "data": data
    }

@app.post("/tourist-spot/update-item/{id}")
async def get_tourist_detail(id, data: TouristSpot):
    mydb = get_database()
    mycol = mydb["tourist_spot"]
    my_query = {"_id": ObjectId(id)}
    new_values = { "$set": { "guide_id": data.guide_id, "name": data.name, "price_tour": data.price_tour, "description": data.description, "sub_title": data.sub_title }}
    result = mycol.update_one(my_query, new_values, upsert=True)
    return {
        "message": "success",
        "data": result.modified_count > 0 or result.upserted_id is not None
    }

if __name__ == '__main__':
    #uvicorn.run(app, host="127.0.0.1", port=8080) #run: python main.py
    uvicorn.run(app, host="127.0.0.1", port=8080, reload=True) #run: uvicorn main:app --reload --port 8080

