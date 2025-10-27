from pydantic import Field
from .base import WithId, TimeStamped

class Produto(WithId, TimeStamped):
    nome: str = Field(min_length=1)
    descricao: str = ""
    preco: float = 0.0
    estoque: int = 0

    # Métodos de domínio (simples)
    def tem_estoque(self, qtd: int) -> bool:
        return self.estoque >= qtd

    def reservar(self, qtd: int) -> bool:
        if self.estoque >= qtd:
            self.estoque -= qtd
            return True
        return False

    def repor(self, qtd: int):
        self.estoque += max(0, qtd)
