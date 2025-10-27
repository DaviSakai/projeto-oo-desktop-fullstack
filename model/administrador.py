from pydantic import Field
from .base import WithId, TimeStamped

class Administrador(WithId, TimeStamped):
    nome: str = Field(min_length=1)
    username: str = Field(min_length=3)
    senha: str = Field(min_length=3)  # simplificado, sem hash

    # Método de domínio
    def validar_login(self, username: str, senha: str) -> bool:
        return self.username == username and self.senha == senha
