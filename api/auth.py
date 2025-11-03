# api/auth.py
from typing import Optional

from fastapi import APIRouter, Request, Response, HTTPException, Depends
from pydantic import BaseModel, EmailStr

from infra.user_repository import UserRepository
from services.auth_service import hash_password, verify_password, SessionStore
from domain.user import User

# Router de autenticação
router = APIRouter(prefix="/auth", tags=["auth"])

# Repositório e sessão (JSON)
repo = UserRepository()
sessions = SessionStore(ttl_minutes=60)

COOKIE_NAME = "session"

# --------- Schemas ---------
class RegisterIn(BaseModel):
    name: str
    email: EmailStr
    password: str

class LoginIn(BaseModel):
    email: EmailStr
    password: str

# --------- Dependência: usuário corrente ---------
def current_user(request: Request) -> Optional[User]:
    token = request.cookies.get(COOKIE_NAME)
    if not token:
        return None
    sess = sessions.get(token)
    if not sess:
        return None
    return repo.get_by_id(sess["user_id"])

# --------- Endpoints ---------
@router.post("/register")
def register(payload: RegisterIn):
    if repo.find_by_email(payload.email):
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")
    pwd_hash = hash_password(payload.password)
    user = User(id=0, name=payload.name, email=payload.email, password_hash=pwd_hash, is_active=True)
    user = repo.create(user)
    return {"id": user.id, "name": user.name, "email": user.email}

@router.post("/login")
def login(payload: LoginIn, response: Response):
    u = repo.find_by_email(payload.email)
    if not u or not verify_password(payload.password, u.password_hash):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    token = sessions.create(u.id)
    response.set_cookie(
        key=COOKIE_NAME,
        value=token,
        httponly=True,
        samesite="lax",
        secure=False,   # True se for HTTPS
        max_age=60*60,
        path="/",
    )
    return {"message": "ok", "user": {"id": u.id, "name": u.name, "email": u.email}}

@router.post("/logout")
def logout(request: Request, response: Response):
    token = request.cookies.get(COOKIE_NAME)
    if token:
        sessions.delete(token)
    response.delete_cookie(COOKIE_NAME, path="/")
    return {"message": "bye"}

@router.get("/me")
def me(user: Optional[User] = Depends(current_user)):
    if not user:
        raise HTTPException(status_code=401, detail="Não autenticado")
    return {"id": user.id, "name": user.name, "email": user.email}
