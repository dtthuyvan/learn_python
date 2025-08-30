from pathlib import Path
from fastapi import FastAPI
from app.routes import employee, home, timekeeping
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI()
app.include_router(home.router)
app.include_router(employee.router)
app.include_router(timekeeping.router)

static_dir = Path(__file__).resolve().parent / "static"
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

if __name__ == '__main__':
    # Recommended: run from project root:
    #   python -m app.main
    # or use uvicorn:
    #   uvicorn app.main:app --reload --port 8000
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
