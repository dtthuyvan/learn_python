from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from app.schemas.user import UserCreate, UserLogin, Token
from app.repositories.user_repository import UserRepository
from app.core.deps import get_db
from app.core.security import verify_password
from app.core.jwt import create_access_token, decode_token, needs_refresh
# ObjectId not needed here; tokens carry string ids

router = APIRouter(prefix="/auth", tags=["auth"])
templates = Jinja2Templates(directory="app/templates")


@router.post("/register", response_model=Token)
def register(user: UserCreate, db = Depends(get_db)):
    repo = UserRepository(db)
    if repo.get_user_by_username(user.username) or repo.get_user_by_email(user.email):
        raise HTTPException(status_code=400, detail="User already exists")
    db_user = repo.create_user(user)
    token = create_access_token(subject=str(db_user.get("_id")))
    return {"access_token": token, "token_type": "bearer"}


@router.post("/refresh", response_model=Token)
def refresh(request: Request, db = Depends(get_db)):
    auth = request.headers.get("Authorization")
    if not auth or not auth.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Missing token")
    token = auth.split(" ", 1)[1]
    try:
        payload = decode_token(token)
    except Exception as exc:
        raise HTTPException(status_code=401, detail="Invalid token") from exc
    if not needs_refresh(payload, within_seconds=300):
        raise HTTPException(status_code=400, detail="Token not within refresh window")
    sub = payload.get("sub")
    new_token = create_access_token(subject=sub)
    return {"access_token": new_token, "token_type": "bearer"}


# -------- Form-based authentication (HTML) --------

@router.get("/login")
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
def login_submit(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db = Depends(get_db),
):
    repo = UserRepository(db)
    user = repo.get_user_by_username(username)
    if not user or not verify_password(password, user.get("hashed_password")):
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Invalid username or password"},
            status_code=400,
        )

    token = create_access_token(subject=str(user.get("_id")))
    response = RedirectResponse(url="/home", status_code=303)
    # HttpOnly cookie for JWT
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax",
        secure=False,
        max_age=15 * 60,
    )
    return response


@router.get("/register")
def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/register-form")
def register_submit(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db = Depends(get_db),
):
    repo = UserRepository(db)
    if repo.get_user_by_username(username) or repo.get_user_by_email(email):
        return templates.TemplateResponse(
            "register.html",
            {"request": request, "error": "User already exists"},
            status_code=400,
        )

    # Create user
    user = UserCreate(username=username, email=email, password=password)
    db_user = repo.create_user(user)

    token = create_access_token(subject=str(db_user.get("_id")))
    response = RedirectResponse(url="/", status_code=303)
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax",
        secure=False,
        max_age=15 * 60,
    )
    return response


@router.get("/logout")
def logout():
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie("access_token")
    return response
