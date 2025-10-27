from fastapi import APIRouter, HTTPException
from typing import Dict, List
from model.pedido import Pedido, DetalhePedido
from model.envio import InformacaoEnvio
from .carrinho_controller import _db as carrinhos_db
from .produto_controller import get_produto_db
from .cliente_controller import get_cliente_db

router = APIRouter(prefix="/pedidos", tags=["pedidos"])

_pedidos: Dict[int, Pedido] = {}
_seq = 1

@router.post("/checkout/{carrinho_id}", response_model=Pedido, status_code=201)
def checkout(carrinho_id: int, envio: InformacaoEnvio):
    global _seq
    car = carrinhos_db.get(carrinho_id)
    if not car: raise HTTPException(404, "Carrinho não encontrado")
    if not car.itens: raise HTTPException(400, "Carrinho vazio")

    cli_db = get_cliente_db()
    if car.cliente_id not in cli_db: raise HTTPException(404, "Cliente não encontrado")

    prod_db = get_produto_db()
    itens: List[DetalhePedido] = []
    for it in car.itens:
        p = prod_db.get(it.numProduto)
        if not p: raise HTTPException(400, f"Produto {it.numProduto} não encontrado")
        itens.append(DetalhePedido(
            numProduto=p.id, nomeProduto=p.nome, quantidade=it.quantidade,
            precoUnit=p.preco, subtotal=round(p.preco*it.quantidade,2)
        ))

    ped = Pedido(id=_seq, cliente_id=car.cliente_id, itens=itens, envio=envio, frete=envio.custo)
    ped.calcular_totais()
    _pedidos[_seq] = ped
    _seq += 1

    # esvazia o carrinho (já reservou estoque ao adicionar; aqui só limpa visualmente)
    car.limpar()
    carrinhos_db[carrinho_id] = car
    return ped

@router.get("", response_model=List[Pedido])
def listar_pedidos():
    return list(_pedidos.values())

@router.get("/{pid}", response_model=Pedido)
def obter_pedido(pid: int):
    p = _pedidos.get(pid)
    if not p: raise HTTPException(404, "Pedido não encontrado")
    return p

@router.patch("/{pid}/estado", response_model=Pedido)
def mudar_estado(pid: int, payload: dict):
    p = _pedidos.get(pid)
    if not p: raise HTTPException(404, "Pedido não encontrado")
    p.estado = payload.get("estado", p.estado)
    _pedidos[pid] = p
    return p
