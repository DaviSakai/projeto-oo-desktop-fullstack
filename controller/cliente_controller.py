from fastapi import APIRouter, HTTPException
from typing import Dict, List
from model.cliente import Cliente

router = APIRouter(prefix="/clientes", tags=["clientes"])

_db: Dict[int, Cliente] = {}
_seq = 1

@router.post("", response_model=Cliente, status_code=201)
def criar_cliente(c: Cliente):
    global _seq
    c.id = _seq
    _seq += 1
    _db[c.id] = c
    return c

@router.get("", response_model=List[Cliente])
def listar_clientes():
    return list(_db.values())

@router.get("/{cid}", response_model=Cliente)
def obter_cliente(cid: int):
    c = _db.get(cid)
    if not c: raise HTTPException(404, "Cliente não encontrado")
    return c

@router.patch("/{cid}", response_model=Cliente)
def atualizar_cliente(cid: int, patch: dict):
    c = _db.get(cid)
    if not c: raise HTTPException(404, "Cliente não encontrado")
    for k, v in patch.items():
        if hasattr(c, k):
            setattr(c, k, v)
    _db[cid] = c
    return c

@router.delete("/{cid}", status_code=204)
def deletar_cliente(cid: int):
    if cid in _db:
        del _db[cid]
        return
    raise HTTPException(404, "Cliente não encontrado")

def get_cliente_db(): return _db
