from pydantic import BaseModel
from typing import Literal

MetodoEnvio = Literal["PAC","SEDEX","Retirada","Entrega Express"]

class InformacaoEnvio(BaseModel):
    destinatario: str
    endereco: str
    cep: str
    metodo: MetodoEnvio = "PAC"
    custo: float = 0.0
    prazoDias: int = 5
