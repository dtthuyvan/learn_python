from fastapi import FastAPI
from routes import employee, home, timekeeping
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI()
app.include_router(home.router)
app.include_router(employee.router)
app.include_router(timekeeping.router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8080) #run: python main.py
    #uvicorn.run(app, host="127.0.0.1", port=8000, reload=True) #run: uvicorn main:app --reload --port 8080
