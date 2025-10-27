from fastapi import APIRouter, HTTPException
from typing import Dict, List
from model.carrinho import Carrinho
from .cliente_controller import get_cliente_db
from .produto_controller import get_produto_db

router = APIRouter(prefix="/carrinhos", tags=["carrinhos"])

_db: Dict[int, Carrinho] = {}
_seq = 1

@router.post("", response_model=Carrinho, status_code=201)
def criar_carrinho(cliente_id: int):
    global _seq
    clientes = get_cliente_db()
    if cliente_id not in clientes:
        raise HTTPException(404, "Cliente não encontrado")

    c = Carrinho(id=_seq, numCarrinho=_seq, cliente_id=cliente_id, itens=[])
    _seq += 1
    _db[c.id] = c

    # vincula no cliente
    cli = clientes[cliente_id]
    cli.carrinho_id = c.id
    clientes[cliente_id] = cli
    return c

@router.get("", response_model=List[Carrinho])
def listar_carrinhos():
    return list(_db.values())

@router.get("/{car_id}", response_model=Carrinho)
def obter_carrinho(car_id: int):
    c = _db.get(car_id)
    if not c: raise HTTPException(404, "Carrinho não encontrado")
    return c

# ⚙️ AÇÃO: adicionar produto (o usuário NÃO chama classe Produto diretamente)
@router.post("/{car_id}/adicionar", response_model=Carrinho)
def adicionar_produto(car_id: int, payload: dict):
    numProduto = int(payload.get("numProduto"))
    quantidade = int(payload.get("quantidade", 1))
    c = _db.get(car_id)
    if not c: raise HTTPException(404, "Carrinho não encontrado")

    produtos = get_produto_db()
    p = produtos.get(numProduto)
    if not p: raise HTTPException(404, "Produto não encontrado")

    if not p.tem_estoque(quantidade):
        raise HTTPException(400, "Estoque insuficiente")

    ok = p.reservar(quantidade)
    if not ok:
        raise HTTPException(400, "Falha ao reservar estoque")

    c.adicionar(numProduto, quantidade)
    _db[car_id] = c
    produtos[p.id] = p
    return c

@router.patch("/{car_id}/quantidade", response_model=Carrinho)
def atualizar_quantidade(car_id: int, payload: dict):
    numProduto = int(payload.get("numProduto"))
    quantidade = int(payload.get("quantidade"))
    c = _db.get(car_id)
    if not c: raise HTTPException(404, "Carrinho não encontrado")
    c.atualizar_qtd(numProduto, quantidade)
    _db[car_id] = c
    return c

@router.delete("/{car_id}/remover/{numProduto}", response_model=Carrinho)
def remover_item(car_id: int, numProduto: int):
    c = _db.get(car_id)
    if not c: raise HTTPException(404, "Carrinho não encontrado")
    c.remover(numProduto)
    _db[car_id] = c
    return c

@router.delete("/{car_id}", status_code=204)
def deletar_carrinho(car_id: int):
    if car_id in _db:
        del _db[car_id]
        return
    raise HTTPException(404, "Carrinho não encontrado")
