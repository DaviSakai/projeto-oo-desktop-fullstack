from datetime import datetime
from pydantic import BaseModel
from .base import WithId, TimeStamped
from typing import List

class ItemCarrinho(BaseModel):
    numProduto: int
    quantidade: int
    dataAdd: datetime = datetime.utcnow()

class Carrinho(WithId, TimeStamped):
    numCarrinho: int | None = None
    cliente_id: int | None = None
    itens: List[ItemCarrinho] = []

    def adicionar(self, numProduto: int, quantidade: int):
        for it in self.itens:
            if it.numProduto == numProduto:
                it.quantidade += quantidade
                return
        self.itens.append(ItemCarrinho(numProduto=numProduto, quantidade=quantidade))

    def atualizar_qtd(self, numProduto: int, quantidade: int):
        for it in self.itens:
            if it.numProduto == numProduto:
                it.quantidade = quantidade
                return

    def remover(self, numProduto: int):
        self.itens = [i for i in self.itens if i.numProduto != numProduto]

    def limpar(self):
        self.itens = []
