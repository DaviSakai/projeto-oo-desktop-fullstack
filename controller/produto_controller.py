from fastapi import APIRouter, HTTPException
from typing import Dict, List
from model.produto import Produto

router = APIRouter(prefix="/produtos", tags=["produtos"])

# "Banco" em memória
_db: Dict[int, Produto] = {}
_seq = 1

@router.post("", response_model=Produto, status_code=201)
def criar_produto(p: Produto):
    global _seq
    p.id = _seq
    _seq += 1
    _db[p.id] = p
    return p

@router.get("", response_model=List[Produto])
def listar_produtos():
    return list(_db.values())

@router.get("/{pid}", response_model=Produto)
def obter_produto(pid: int):
    p = _db.get(pid)
    if not p: raise HTTPException(404, "Produto não encontrado")
    return p

@router.patch("/{pid}", response_model=Produto)
def atualizar_produto(pid: int, patch: dict):
    p = _db.get(pid)
    if not p: raise HTTPException(404, "Produto não encontrado")
    for k, v in patch.items():
        if hasattr(p, k):
            setattr(p, k, v)
    _db[pid] = p
    return p

@router.delete("/{pid}", status_code=204)
def deletar_produto(pid: int):
    if pid in _db:
        del _db[pid]
        return
    raise HTTPException(404, "Produto não encontrado")

# Helpers p/ outros controllers
def get_produto_db(): return _db
