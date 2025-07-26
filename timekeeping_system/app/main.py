from fastapi import FastAPI
from app.routes import employee, home, timekeeping
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.include_router(home.router)
app.include_router(employee.router)
app.include_router(timekeeping.router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
