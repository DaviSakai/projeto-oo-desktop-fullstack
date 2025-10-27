from fastapi import APIRouter, HTTPException
from typing import Dict, List
from model.administrador import Administrador

router = APIRouter(prefix="/administradores", tags=["administradores"])

_db: Dict[int, Administrador] = {}
_seq = 1

@router.post("", response_model=Administrador, status_code=201)
def criar_admin(a: Administrador):
    global _seq
    a.id = _seq
    _seq += 1
    _db[a.id] = a
    return a

@router.get("", response_model=List[Administrador])
def listar_admins():
    return list(_db.values())

@router.post("/login")
def login(payload: dict):
    username = payload.get("username")
    senha = payload.get("senha")
    for a in _db.values():
        if a.validar_login(username, senha):
            return {"ok": True, "admin_id": a.id, "nome": a.nome}
    raise HTTPException(401, "Credenciais inválidas")

def get_admin_db(): return _db
