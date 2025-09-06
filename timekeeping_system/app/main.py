from pathlib import Path
from fastapi import FastAPI, Request
from app.routes import employee, home, timekeeping, auth
from fastapi.staticfiles import StaticFiles
import uvicorn
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import RedirectResponse
from app.core.jwt import decode_token

app = FastAPI()


async def jwt_middleware(request: Request, call_next):
    path = request.url.path
    # Public paths and prefixes that don't require authentication
    public_paths = {
        "/",
        "/home",  # allow navigation target; enforcement relies on presence of token
        "/auth/login",
        "/auth/register",
        "/auth/register-form",
        "/auth/refresh",
        "/auth/logout",
    }
    public_prefixes = (
        "/static",
        "/employees",
        "/timekeeping",
    )

    if path in public_paths or any(path.startswith(p) for p in public_prefixes):
        response = await call_next(request)
        return response

    token = request.cookies.get("access_token")
    if not token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.lower().startswith("bearer "):
            token = auth_header.split(" ", 1)[1]

    if not token:
        return RedirectResponse(url="/auth/login", status_code=303)

    try:
        payload = decode_token(token)
        # Optionally expose user info to downstream handlers
        request.state.user_id = payload.get("sub")
    except Exception:
        return RedirectResponse(url="/auth/login", status_code=303)

    response = await call_next(request)
    return response


app.add_middleware(BaseHTTPMiddleware, dispatch=jwt_middleware)
app.include_router(home.router)
app.include_router(employee.router)
app.include_router(timekeeping.router)
app.include_router(auth.router)

static_dir = Path(__file__).resolve().parent / "static"
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

if __name__ == '__main__':
    # Recommended: run from project root:
    #   python -m app.main
    # or use uvicorn:
    #   uvicorn app.main:app --reload --port 8000
    uvicorn.run("app.main:app", host="127.0.0.1", port=9000, reload=True)