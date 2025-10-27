from datetime import datetime
from pydantic import BaseModel
from typing import List, Literal
from .envio import InformacaoEnvio

EstadoPedido = Literal["CRIADO","PAGO","EM_SEPARACAO","ENVIADO","ENTREGUE","CANCELADO"]

class DetalhePedido(BaseModel):
    numProduto: int
    nomeProduto: str
    quantidade: int
    precoUnit: float
    subtotal: float

class Pedido(BaseModel):
    id: int | None = None
    cliente_id: int
    created_at: datetime = datetime.utcnow()
    estado: EstadoPedido = "CRIADO"
    itens: List[DetalhePedido] = []
    totalProdutos: float = 0.0
    frete: float = 0.0
    totalGeral: float = 0.0
    envio: InformacaoEnvio | None = None

    def calcular_totais(self):
        self.totalProdutos = round(sum(i.subtotal for i in self.itens), 2)
        self.totalGeral = round(self.totalProdutos + (self.frete or 0.0), 2)
