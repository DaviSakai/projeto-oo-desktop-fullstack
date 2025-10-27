from pydantic import EmailStr, Field
from .base import WithId, TimeStamped
from typing import List

class Cliente(WithId, TimeStamped):
    nomeCliente: str = Field(min_length=1)
    email: EmailStr
    endereco: str = ""
    infoEnvio: str = ""
    saldoConta: float = 0.0
    carrinho_id: int | None = None

    # Métodos de domínio (simples)
    def creditar(self, valor: float):
        self.saldoConta += max(0.0, valor)

    def debitar(self, valor: float) -> bool:
        if valor <= self.saldoConta:
            self.saldoConta -= valor
            return True
        return False
